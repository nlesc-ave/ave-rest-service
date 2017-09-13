import connexion
from flask import current_app

from ..db import get_db
from ..features import featurebb2label, find_features
from ..genes import find_genes
from ..sequence import get_chrominfo
from ..variants import get_accessions_list, AccessionsLookupError
from ..variants import get_haplotypes
from ..whoosh import get_woosh_dir


def get(genome_id):
    try:
        genome_info = {
            'genome_id': genome_id,
            'chromosomes': chromosomes(genome_id),
            'feature_tracks': feature_tracks(genome_id),
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


def feature_tracks(genome_id):
    db = get_db()
    query = """SELECT filename
               FROM metadata
               WHERE genome=? AND datatype='features'"""
    cursor = db.cursor()
    tracks = []
    for row in cursor.execute(query, (genome_id, )):
        url = row[0]
        label = featurebb2label(url)
        track = {
            'label': label,
            'url': url
        }
        tracks.append(track)
    return tracks


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
               WHERE genome=? AND datatype='genes'"""
    cursor = db.cursor()
    cursor.execute(query, (genome_id, ))
    result = cursor.fetchone()
    if result is None:
        return None
    filename = result['filename']
    return filename


def haplotypes(genome_id, chrom_id, start_position, end_position, accessions=None):
    """
    Calculate haplotypes for chosen region and set of accessions.
    """
    # if region is too big refuse, return error
    requested_range = end_position - start_position
    max_range = int(current_app.config['MAX_RANGE'])
    if requested_range > max_range:
        message = 'Requested range {0} is larger than maximum allowed range {1}'.format(requested_range, max_range)
        return connexion.problem(406, "Not Acceptable", message)

    db = get_db()
    # to construct haplotypes, both:
    # variants from bcf file and
    # reference sequence from 2bit
    # are needed

    query = """SELECT filename
               FROM metadata
               WHERE genome=? AND datatype='variants'"""
    cursor = db.cursor()
    cursor.execute(query, (genome_id, ))
    variants_row = cursor.fetchone()
    if variants_row is None:
        ext = {'genome_id': genome_id}
        message = "Genome with id \'{0}\' contains no variants".format(genome_id)
        return connexion.problem(404, "Not Found", message, ext=ext)
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
        message = "Genome with id \'{0}\' not found".format(genome_id)
        return connexion.problem(404, "Not Found", message, ext=ext)

    ref_file = ref_row['filename']

    if accessions is None:
        accessions = []

    try:
        return get_haplotypes(variant_file, ref_file, chrom_id, start_position, end_position, accessions)
    except AccessionsLookupError as e:
        ext = {'genome_id': genome_id, 'accessions': list(e.accessions)}
        return connexion.problem(404, "Not Found", "Some accessions not found", ext=ext)


def gene_search(genome_id, query):
    # first we need to mach all big bed files for this genome
    # based on info in metadata sqlite table
    db = get_db()
    sql_query = """SELECT filename
               FROM metadata
               WHERE genome=? AND datatype='genes'"""
    cursor = db.cursor()
    cursor.execute(sql_query, (genome_id, ))
    row = cursor.fetchone()
    if row is None:
        ext = {'genome_id': genome_id}
        return connexion.problem(404, "Not Found", "Genome with id \'{0}\' not found".format(genome_id), ext=ext)

    genes_file = row['filename']

    # then we'll find out what is the whoosh path for index of this bigbed file
    whoosh_base_dir = current_app.config['WHOOSH_BASE_DIR']
    whoosh_dir = get_woosh_dir(genes_file, whoosh_base_dir)
    return find_genes(whoosh_dir, query)


def feature_search(genome_id, query):
    # first we need to mach all big bed files for this genome
    # based on info in metadata sqlite table
    db = get_db()
    sql_query = """SELECT filename
               FROM metadata
               WHERE genome=? AND datatype='features'"""
    cursor = db.cursor()
    cursor.execute(sql_query, (genome_id, ))
    row = cursor.fetchone()
    if row is None:
        ext = {'genome_id': genome_id}
        return connexion.problem(404, "Not Found", "Genome with id \'{0}\' not found".format(genome_id), ext=ext)

    whoosh_base_dir = current_app.config['WHOOSH_BASE_DIR']
    whoosh_dir = get_woosh_dir(genome_id + '-features', whoosh_base_dir)
    return find_features(whoosh_dir, query)
