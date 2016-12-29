import pysam
from pysam import VariantFile
from pysam import TabixFile
from pyfaidx import Fasta

# tomato data files
reference_file = 'S_lycopersicum_chromosomes.2.40.fa'
annotation_file = 'gene_models.gff.gz'
variant_file = 'tomato_snps.bcf'

# load reference sequence
reference = Fasta(reference_file)

# load gene annotations
annotations = TabixFile(annotation_file)

# laod variant annotations
variants = VariantFile(variant_file)

# regions to query
region1 = ('SL2.40ch01', 15000, 21000)
region2 = ('SL2.40ch01', 20000, 70000)

# queries

region1_reference = reference[region1[0]][region1[1]: region1[2]]
region1_annotations = [a for a in annotations.fetch(*region1, parser=pysam.asGTF())]
region1_variants = [a for a in variants.fetch(*region1)]

region2_reference = reference[region2[0]][region2[1]: region2[2]]
region2_annotations = [a for a in annotations.fetch(*region2, parser=pysam.asGTF())]
region2_variants = [a for a in variants.fetch(*region2)]

# arabidopsis data files
reference_file = 'TAIR10.fa'
annotation_file = 'TAIR10_GFF3_genes.sorted.gff.gz'
variant_file = 'at_variants_sorted.bcf'

# load reference sequence
reference = Fasta(reference_file)

# load gene annotations
annotations = TabixFile(annotation_file)

# regions to query
region1 = ('2', 35000, 45000)


# queries
region1_reference = reference[region1[0]][region1[1]: region1[2]]
region1_annotations = [a for a in annotations.fetch(*region1, parser=pysam.asGTF())]
region1_variants = [a for a in variants.fetch(*region1)]