from os import linesep
from subprocess import check_output, CalledProcessError, PIPE


class InvalidChromosome(LookupError):
    def __init__(self, file_name, chrom_id):
        super().__init__()
        self.file_name = file_name
        self.chrom_id = chrom_id


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
    """Retrieve sequence of a region in a 2bit file

    Args:
        filename: Filename of 2bit file
        chrom_id: Chromosome identifier
        start_position: Start at given position in sequence (zero-based)
        end_position: End at given position in sequence (non-inclusive)

    Returns:
        DNA sequence as a string
    """
    args = (
        'twoBitToFa',
        '-seq=' + chrom_id,
        '-start=' + str(start_position),
        '-end=' + str(end_position),
        filename,
        'stdout'
    )
    try:
        fasta = check_output(args, stderr=PIPE).decode('ascii')
        header = '>' + chrom_id + ':' + \
            str(start_position) + '-' + str(end_position) + linesep
        return fasta.replace(header, '').replace(linesep, '')
    except CalledProcessError as e:
        if 'is not in' in e.stderr.decode('ascii'):
            raise InvalidChromosome(filename, chrom_id)
        else:
            raise e
