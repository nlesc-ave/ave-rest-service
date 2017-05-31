from cyvcf2 import VCF

def get_accessions_list(filename):
    variants = VCF(filename)
    return variants.samples
