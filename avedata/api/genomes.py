import connexion

from ..db import get_db
from ..features import get_annotations
from ..features import get_featuretypes
from ..features import get_genes
from ..sequence import get_chrominfo
from ..variants import get_accessions_list, AccessionsLookupError
from ..variants import get_haplotypes


def get(genome_id):
    try:
        genome_info = {
            'genome_id': genome_id,
            'chromosomes': chromosomes(genome_id),
            'feature_types': featuretypes(genome_id),
            'accessions': accession_list(genome_id),
            'reference': two_bit_uri(genome_id),
        }
        gene_track = gene_track_uri(genome_id)
        if gene_track:
            genome_info['gene_track'] = gene_track
        return genome_info
    except LookupError:
        ext = {'genome_id': genome_id}
        return connexion.problem(404, "Not Found", "Genome with id \'{0}\' not found".format(genome_id), ext=ext)


def chromosomes(genome_id):
    """Fetch 2bit file name for this genome
        open file with twoBitInfo
        get list of chromosomes and fetch their 'chrom_id': len
        return [{'chrom_id': length},]
    """
    db = get_db()
    query = """SELECT filename
               FROM metadata
               WHERE genome=? AND datatype='2bit'"""
    cursor = db.cursor()
    cursor.execute(query, (genome_id, ))
    result = cursor.fetchone()
    if result is None:
        raise LookupError()
    filename = result[0]
    return get_chrominfo(filename)


def featuretypes(genome_id):
    db = get_db()
    query = """SELECT filename
               FROM metadata
               WHERE genome=? AND datatype='features'"""
    cursor = db.cursor()
    cursor.execute(query, (genome_id, ))
    result = cursor.fetchone()
    if result is None:
        return []
    filename = result[0]
    return get_featuretypes(filename)


def accession_list(genome_id):
    db = get_db()
    query = """SELECT filename
               FROM metadata
               WHERE genome=? AND datatype='variants'"""
    cursor = db.cursor()
    cursor.execute(query, (genome_id, ))
    result = cursor.fetchone()
    if result is None:
        return []
    filename = result[0]
    return get_accessions_list(filename)


def two_bit_uri(genome_id):
    db = get_db()
    query = """SELECT filename
               FROM metadata
               WHERE genome=? AND datatype='2bit'"""
    cursor = db.cursor()
    cursor.execute(query, (genome_id, ))
    result = cursor.fetchone()
    if result is None:
        raise LookupError()
    filename = result['filename']
    return filename


def gene_track_uri(genome_id):
    db = get_db()
    query = """SELECT filename
               FROM metadata
               WHERE genome=? AND datatype='bigbed'"""
    cursor = db.cursor()
    cursor.execute(query, (genome_id, ))
    result = cursor.fetchone()
    if result is None:
        return None
    filename = result['filename']
    return filename


def genes(genome_id, chrom_id, start_position, end_position):
    """Fetch all gene annototion information for particular location.
    Return list of dicts with gff information."""
    db = get_db()
    query = """SELECT filename
               FROM metadata
               WHERE genome=? AND datatype='features'"""
    cursor = db.cursor()
    cursor.execute(query, (genome_id, ))
    filename = cursor.fetchone()['filename']
    return get_genes(filename, chrom_id, start_position, end_position)


def features(genome_id, chrom_id, start_position, end_position):
    """Fetch genomic features of selected genomes
    Return list of genomic features.
    """
    db = get_db()
    query = """SELECT filename
               FROM metadata
               WHERE genome=? AND datatype='features'"""
    cursor = db.cursor()
    cursor.execute(query, (genome_id, ))
    filename = cursor.fetchone()['filename']
    return get_annotations(filename, chrom_id, start_position, end_position)


def haplotypes(genome_id, chrom_id, start_position, end_position, accessions=None):
    """
    Calculate haplotypes for chosen region and set of accessions.
    """
    db = get_db()
    # to construct haplotypes, both:
    # variants from bcf file and
    # reference sequence from 2bit (or fasta)
    # are needed

    query = """SELECT filename
               FROM metadata
               WHERE genome=? AND datatype='variants'"""
    cursor = db.cursor()
    cursor.execute(query, (genome_id, ))
    variants_row = cursor.fetchone()
    if variants_row is None:
        ext = {'genome_id': genome_id}
        return connexion.problem(404, "Not Found", "Genome with id \'{0}\' contains no variants".format(genome_id), ext=ext)
    variant_file = variants_row['filename']

    query = """SELECT filename
            FROM metadata
            WHERE genome=?
            AND datatype='2bit'"""
    cursor = db.cursor()
    cursor.execute(query, (genome_id, ))
    ref_row = cursor.fetchone()
    if ref_row is None:
        ext = {'genome_id': genome_id}
        return connexion.problem(404, "Not Found", "Genome with id \'{0}\' not found".format(genome_id), ext=ext)

    ref_file = ref_row['filename']

    if accessions is None:
        accessions = []

    try:
        return get_haplotypes(variant_file, ref_file, chrom_id, start_position, end_position, accessions)
    except AccessionsLookupError as e:
        ext = {'genome_id': genome_id, 'accessions': e.accessions}
        msg = "Not Found", "Accessions {1} of genome with id \'{0}\' not found".format(genome_id, e.accessions)
        return connexion.problem(404, msg, ext=ext)


def gene_search(genome_id, query):
    raise NotImplementedError()


def feature_search(genome_id, query):
    raise NotImplementedError()
