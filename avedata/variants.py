from cyvcf2 import VCF
from Levenshtein import hamming

def get_accessions_list(filename):
    variants = VCF(filename)
    return variants.samples

def get_haplotypes(filename, chrom_id, start_position, end_position, accessions):
    region = '{0}:{1}-{2}'.format(chrom_id, start_position, end_position)
    vcf = VCF(filename)
    variants = vcf(region)
    accessions = vcf.samples
    sequences = ['' for a in accessions]
    for v in variants:
        if v.is_snp:
            for accession_idx, genotype in enumerate(v.genotypes):
                if genotype[0] == -1:
                    sequences[accession_idx] += v.REF
                else:
                    # ignores heterozygosity
                    # always picks most frequent ALT
                    sequences[accession_idx] += v.ALT[0]
    # concatenate sequences into strings
    # sequences = [''.join(s) for s in sequences]
    acc1_list = []
    acc2_list = []
    distances_list = []
    for acc1_idx, acc1 in enumerate(accessions):
        for acc2_idx, acc2 in enumerate(accessions):
            acc1_list.append(acc1)
            acc2_list.append(acc2)
            seq1 = sequences[acc1_idx]
            seq2 = sequences[acc2_idx]
            distances_list.append(hamming(seq1, seq2))

    return distances_list



    hierarchy = {'haplotype_id': '',
                 'children': accessions}
