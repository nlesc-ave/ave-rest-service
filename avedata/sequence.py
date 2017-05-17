from pyfaidx import Fasta

def get_chrominfo(filename):
    """Get list of chromosome ids and their lengths"""
    chromosomes = Fasta(filename)
    chrominfo = [{'chrom_id': chrom_id, 'length': len(chromosomes[chrom_id])}
                 for chrom_id in chromosomes.keys()]
    return chrominfo

def get_reference(filename, chrom_id, start_position, end_position):
    """Fetch reference sequence of genomic region"""
    chromosomes = Fasta(filename)
    reference = chromosomes[chrom_id][start_position:end_position].seq
    return reference
