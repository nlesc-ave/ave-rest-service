from cyvcf2 import VCF

def get_accessions_list(filename):
    variants = VCF(filename)
    return variants.samples

def get_haplotypes(filename, chrom_id, start_position, end_position, accessions):
    region = '{0}:{1}-{2}'.format(chrom_id, start_position, end_position)
    vcf = VCF(filename)
    variants = vcf(region)
    accessions = vcf.samples
    sequences = [[] for a in accessions]
    for pos, variant in enumerate(variants):
        if variant.is_snp:
            for accession_idx, genotype in enumerate(variant.genotypes):
                if genotype[0] == -1:
                    sequences[accession_idx].append(variant.REF)
                else:
                    # ignores heterozygosity
                    # always picks most frequent ALT
                    sequences[accession_idx].append(variant.ALT[0])
    # concatenate sequences into strings
    sequences = [''.join(s) for s in sequences]
    return sequences



    hierarchy = {'haplotype_id': '',
                 'children': accessions}
