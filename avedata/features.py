import pysam
from pysam import TabixFile


def get_featuretypes(filename):
    """Return a list of all types of features in
       registered gff file"""
    gff = TabixFile(filename, parser=pysam.asGTF())
    featuretypes = set()
    for f in gff.fetch():
        featuretypes.add(f.feature)
    return list(featuretypes)
