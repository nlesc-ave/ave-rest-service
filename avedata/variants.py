import uuid
from cyvcf2 import VCF
import pandas as pd
import numpy as np
import scipy.cluster.hierarchy as hcl
import scipy.cluster
from itertools import combinations, permutations
from collections import defaultdict
from functools import reduce

from avedata.sequence import get_sequence


def scipyclust2json(clusters, labels):
    T = scipy.cluster.hierarchy.to_tree( clusters , rd=False )

    # Create dictionary for labeling nodes by their IDs
    id2name = dict(zip(range(len(labels)), labels))

    # Create a nested dictionary from the ClusterNode's returned by SciPy
    def add_node(node, parent ):
        # First create the new node and append it to its parent's children
        newNode = dict( node_id=node.id, children=[] )
        parent["children"].append( newNode )

        # Recursively add the current node's children
        if node.left: add_node( node.left, newNode )
        if node.right: add_node( node.right, newNode )

    # Initialize nested dictionary for d3, then recursively iterate through tree
    d3Dendro = dict(children=[])
    add_node( T, d3Dendro )

    ordered_haplotype_ids = []

    # Label each node with the names of each leaf in its subtree
    def label_tree( n ):
        # If the node is a leaf, then we have its name
        if len(n["children"]) == 0:
            n['haplotype_id'] = id2name[n["node_id"]]
            ordered_haplotype_ids.append(n['haplotype_id'])
            del n['children']
            leafNames = [ id2name[n["node_id"]] ]

        # If not, flatten all the leaves in the node's subtree
        else:
            leafNames = reduce(lambda ls, c: ls + label_tree(c), n["children"], [])

        # Delete the node id since we don't need it anymore and
        # it makes for cleaner JSON
        del n["node_id"]

        return leafNames

    label_tree( d3Dendro["children"][0] )
    return d3Dendro, ordered_haplotype_ids


def get_accessions_list(filename):
    variants = VCF(filename)
    return variants.samples


class AccessionsLookupError(LookupError):
    def __init__(self, accessions):
        super().__init__()
        self.accessions = accessions


def get_haplotypes(variant_file, ref_file, chrom_id, start_position, end_position, accessions):
    region = '{0}:{1}-{2}'.format(chrom_id, start_position, end_position)
    vcf = VCF(variant_file)
    vcf_variants = vcf(region)
    all_accessions = vcf.samples
    if len(accessions) == 0:
        accessions = all_accessions

    if not set(accessions).issubset(set(all_accessions)):
        raise AccessionsLookupError(set(accessions).difference(set(all_accessions)))

    # sequences in a dictionar
    # with accession names as keys
    sequences = defaultdict(str)
    # positions of the variants in a dictionary
    # fetch the genotypes in the variation positions
    # store all the variant objects in an array
    variants = []
    for v in vcf_variants:
        if v.is_snp:
            variant = {
                'chrom': v.CHROM,
                'pos': v.POS,
                'id': v.ID,
                'ref': v.REF,
                'alt': v.ALT,
                'qual': v.QUAL,
                'filter': v.FILTER,
                'info': dict(v.INFO),
                'genotypes': []
            }
            for idx, (acc, genotype) in enumerate(zip(all_accessions, v.genotypes)):
                if acc not in accessions:
                    continue
                if genotype[0] == -1:
                    sequences[acc] += v.REF
                else:
                    # ignores heterozygosity
                    # always picks most frequent ALT
                    sequences[acc] += v.ALT[0]
                    # add info to variant object
                    # genotype should contain all format fields for each
                    # actual varint at this position
                    genotype = {
                        'accession': acc,
                        'genotype': str(genotype[:2])
                    }
                    for f in v.FORMAT[1:]:
                        genotype[f] = str(v.format(f)[idx])
                    variant['genotypes'].append(genotype)
            variants.append(variant)

    # concatenate sequences into strings
    # sequences = [''.join(s) for s in sequences]
    acc1_list = []
    acc2_list = []
    distances_list = []

    haplotypes = {}
    if len(accessions) == 1:
        haplotype_id = uuid.uuid4().hex
        haplotypes[haplotype_id] = {'accessions': [accessions[0]]}
    else:
        # calculate distances for all the accession pairs
        for acc1, acc2 in permutations(accessions, 2):
            acc1_list.append(acc1)
            acc2_list.append(acc2)
            seq1 = sequences[acc1]
            seq2 = sequences[acc2]
            if seq1 == seq2:
                distances_list.append(0)
            else:
                distances_list.append(1)

        # create a pandas dataframe with the distances
        # between each accession
        dists = pd.DataFrame({
            "acc1": acc1_list,
            "acc2": acc2_list,
            "distance": distances_list
        })

        # get list of accessions in each haplotype
        accessions_set = set(dists['acc1'])

        # group accessions into haplotypes
        while len(accessions_set):
            # get one accession from the set
            acc = accessions_set.pop()
            # get all the comparisons with this accession
            single_accession = dists[(dists['acc1'] == acc)]
            # fetch rows with zero distance
            zero_distance = single_accession[(single_accession['distance'] == 0)]
            haplotype_accessions = list(zero_distance['acc2'])
            unique_ha = []
            for ha in haplotype_accessions:
                if ha in accessions_set:
                    unique_ha.append(ha)
                    # those accession cannot be in any other haplotype
                    # remove them from the set
                    accessions_set.discard(ha)
            unique_ha.append(acc)
            # generate unique labels for the haplotypes
            haplotype_id = uuid.uuid4().hex
            haplotypes[haplotype_id] = {'accessions': unique_ha}

    # add variant information to haplotypes
    # variants should only contain genotype information
    # about genotypes present in particular haplotype
    for h_id, haplotype in haplotypes.items():
        haplotype['variants'] = []
        for v in variants:
            genotypes = []
            for g in v['genotypes']:
                if g['accession'] in haplotype['accessions']:
                    genotypes.append(g)
            if len(genotypes):
                haplotype_variant = v
                haplotype_variant['genotypes'] = genotypes
                haplotypes[h_id]['variants'].append(haplotype_variant)

    # load reference sequence from a 2bit file
    ref_seq = get_sequence(ref_file, chrom_id, start_position, end_position)

    # reconstruct the sequence based on reference and variant information of the
    # haplotype; both the sequence (a python string) and the variants from vcf
    # are indexed from zero
    for h in haplotypes.values():
        haplotype_sequence = list(ref_seq)
        for v in h['variants']:
            # TODO start_position is 1-based, while seq and vcf is 0-based, require -1 | +1 ?
            haplotype_sequence[v['pos'] - start_position] = v['alt'][0]
        h['sequence'] = "".join(haplotype_sequence)

    # get distances between the haplotypes based on the distances between
    # the accessions
    haplotype_ids = list(haplotypes.keys())
    haplotype_distances = []

    # if there is just one haplotype, due to for example no variants in region, then hierarchy will be a single node
    if len(haplotype_ids) < 2:
        haplotype_id = haplotype_ids[0]
        haplotype = haplotypes[haplotype_id]
        haplotype['haplotype_id'] = haplotype_id
        return {
            'haplotypes': [
                haplotype
            ],
            'hierarchy': {
                'haplotype_id': haplotype_id
            }
        }

    for h1, h2 in combinations(haplotype_ids, 2):
        # get name of the first accession in both compared haplotypes
        acc1 = haplotypes[h1]['accessions'][0]
        acc2 = haplotypes[h2]['accessions'][0]
        # get distance between those based on dists df
        df1 = dists[(dists['acc1'] == acc1)]
        df2 = df1[(df1['acc2'] == acc2)]
        dist = df2.iloc[0]['distance']
        haplotype_distances.append(dist)

    clusters = hcl.linkage(np.array(haplotype_distances))
    root_node, ordered_haplotype_ids = scipyclust2json(clusters, haplotype_ids)
    ordered_haplotypes = []
    for haplotype_id in ordered_haplotype_ids:
        haplotype = haplotypes[haplotype_id]
        haplotype['haplotype_id'] = haplotype_id
        ordered_haplotypes.append(haplotype)

    return {
        'hierarchy': root_node,
        'haplotypes': ordered_haplotypes
    }
