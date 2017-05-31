import pysam
from pysam import TabixFile

GENE_FEATURES = ['CDS', 'exon', 'five_prime_UTR', 'gene', 'intron',
                'mRNA', 'three_prime_UTR']

def attributes_dict_from_string(attributes_string):
    """Convert a string with attributes to a dictionary"""
    attributes_dict = {}
    key_value_list = attributes_string.split(";")
    for key_value in key_value_list:
        key, value = key_value.split("=")
        attributes_dict[key] = value
    return attributes_dict

def dict_from_gff(gff):
    gff_dict={
        'seqid': gff.contig,
        'source': gff.source,
        'type': gff.feature,
        'start': gff.start,
        'end': gff.end,
        'score': gff.score,
        'strand': gff.strand,
        'phase': gff.frame,
        'attributes': attributes_dict_from_string(gff.keys()[0])
    }
    return gff_dict

def get_featuretypes(filename):
    """Return a list of all types of features in
       registered gff file"""
    gff = TabixFile(filename, parser=pysam.asGTF())
    featuretypes = set()
    for f in gff.fetch():
        if f.feature not in GENE_FEATURES:
            featuretypes.add(f.feature)
    return list(featuretypes)

def get_genes(filename, chrom_id, start_position, end_position):
    """Fetch genes from defined region"""
    gene_features = ['CDS', 'exon', 'five_prime_UTR', 'gene', 'intron',
                     'mRNA', 'three_prime_UTR']
    gff = TabixFile(filename, parser=pysam.asGTF())
    genes = [gene for gene in gff.fetch(chrom_id, start_position, end_position)
             if gene.feature in GENE_FEATURES]
    genes = [dict_from_gff(g) for g in genes]
    print(len(genes))
    return genes

def get_annotations(filename, chrom_id, start_position, end_position):
    """Fetch genes from defined region"""
    featuretypes = ['CDS', 'exon', 'five_prime_UTR', 'gene', 'intron',
                     'mRNA', 'three_prime_UTR']
    gff = TabixFile(filename, parser=pysam.asGTF())
    annotations = [annotation
                   for annotation in gff.fetch(chrom_id, start_position, end_position)
                   if annotation.feature not in featuretypes]
    annotations = [dict_from_gff(a) for a in GENE_FEATURES]
    return annotations
