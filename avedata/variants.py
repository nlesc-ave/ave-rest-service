import uuid
from cyvcf2 import VCF
from Levenshtein import hamming
import pandas as pd
import numpy as np
import scipy.cluster.hierarchy as hcl
import scipy.cluster
from scipy.spatial.distance import squareform
from itertools import combinations, permutations
from collections import defaultdict
from functools import reduce
import twobitreader as tbr

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
    d3Dendro = dict(children=[], name="Root1")
    add_node( T, d3Dendro )

    # Label each node with the names of each leaf in its subtree
    def label_tree( n ):
        # If the node is a leaf, then we have its name
        if len(n["children"]) == 0:
            leafNames = [ id2name[n["node_id"]] ]

        # If not, flatten all the leaves in the node's subtree
        else:
            leafNames = reduce(lambda ls, c: ls + label_tree(c), n["children"], [])

        # Delete the node id since we don't need it anymore and
        # it makes for cleaner JSON
        del n["node_id"]

        # Labeling convention: "-"-separated leaf names
        n["name"] = name = "-".join(sorted(map(str, leafNames)))

        return leafNames

    label_tree( d3Dendro["children"][0] )
    return d3Dendro


def get_accessions_list(filename):
    variants = VCF(filename)
    return variants.samples

def get_haplotypes(variant_file, ref_file, chrom_id, start_position, end_position, accessions):
    region = '{0}:{1}-{2}'.format(chrom_id, start_position, end_position)
    vcf = VCF(variant_file)
    vcf_variants = vcf(region)
    accessions = vcf.samples
    # sequences in a dictionar
    # with accession names as keys
    sequences = defaultdict(str)
    # positions of the variants in a dictionary
    # fetch the genotypes in the variation positions
    # store all the variant objects in an array
    variants = []
    for v in vcf_variants:
        #
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
        if v.is_snp:
            for idx, (acc, genotype) in enumerate(zip(accessions, v.genotypes)):
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
    # calculate distances for all the accession pairs
    for acc1, acc2 in permutations(accessions, 2):
        acc1_list.append(acc1)
        acc2_list.append(acc2)
        seq1 = sequences[acc1]
        seq2 = sequences[acc2]
        distances_list.append(hamming(seq1, seq2))

    # create a pandas dataframe with the distances
    # between each accession
    dists = pd.DataFrame({
        "acc1": acc1_list,
        "acc2": acc2_list,
        "distance": distances_list
    })

    # get list of accessions in each haplotype
    accessions_set = set(dists['acc1'])
    haplotypes = {}

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
                # those accesssion cannot be in any other haplotype
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
        haplotypes[h_id]['variants'] = []
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
    f = tbr.TwoBitFile(ref_file)
    chromosome = f[chrom_id]
    ref_seq = chromosome[start_position:end_position]

    # reconstruct the sequence based on reference and variant information of the
    # haplotype; both the sequence (a python string) and the variants from vcf
    # are indexed from zero
    for h in haplotypes.values():
        haplotype_sequence = list(ref_seq)
        for v in haplotype['variants']:
            haplotype_sequence[v['pos']] = v['alt'][0]
        h['sequence'] = "".join(haplotype_sequence)

    # get distances between the haplotypes based on the distances between
    # the accessions
    haplotype_ids = list(haplotypes.keys())
    haplotype_distances = []

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

    return clusters, haplotype_ids



    hierarchy = {'haplotype_id': '',
                 'children': accessions}
