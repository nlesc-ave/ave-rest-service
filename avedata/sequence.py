from os import linesep
from subprocess import check_output


def get_chrominfo(filename):
    """Get list of chromosome ids and their lengths"""
    args = (
        'twoBitInfo',
        filename,
        'stdout'
    )
    tabulated_chromosomes = check_output(args).decode('ascii')
    chromosomes = []
    for line in tabulated_chromosomes.splitlines():
        (chrom_id, length) = line.split('\t')
        chromosomes.append({'chrom_id': chrom_id, 'length': int(length)})
    return chromosomes


def get_sequence(filename, chrom_id, start_position, end_position):
    args = (
        'twoBitToFa',
        '-seq=' + chrom_id,
        '-start=' + str(start_position),
        '-end=' + str(end_position),
        filename,
        'stdout'
    )
    fasta = check_output(args).decode('ascii')
    header = '>' + chrom_id + ':' + str(start_position) + '-' + str(end_position) + linesep
    return fasta.replace(header, '').replace(linesep, '')
