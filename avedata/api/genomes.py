from ..db import get_db
from ..sequence import get_chrominfo
from ..sequence import get_reference
from ..features import get_genes
from ..features import get_annotations
from ..features import get_featuretypes
from ..variants import get_accessions_list
from ..variants import get_haplotypes

def get(genome_id):

    genome_info = {
        'genome_id': genome_id,
        'chromosomes': chromosomes(genome_id),
        'feature_types': featuretypes(genome_id),
        'accessions': accession_list(genome_id),
        'reference': two_bit_uri(genome_id),
        'gene_track': gene_track_uri(genome_id)
    }
    return genome_info

def chromosomes(genome_id):
    """Fetch fasta file name for this genome
        open file with pyfaidx
        get list of chromosomes and fetch their 'chrom_id': len
        return [{'chrom_id': length},]
    """
    db = get_db()
    query = """SELECT filename
               FROM metadata
               WHERE genome=? AND datatype='sequence'"""
    cursor = db.cursor()
    cursor.execute(query, (genome_id, ))
    filename = cursor.fetchone()[0]
    chrominfo = get_chrominfo(filename)
    return chrominfo

def featuretypes(genome_id):
    db = get_db()
    query = """SELECT filename
               FROM metadata
               WHERE genome=? AND datatype='features'"""
    cursor = db.cursor()
    cursor.execute(query, (genome_id, ))
    filename = cursor.fetchone()[0]
    return get_featuretypes(filename)

def accession_list(genome_id):
    db = get_db()
    query = """SELECT filename
               FROM metadata
               WHERE genome=? AND datatype='variants'"""
    cursor = db.cursor()
    cursor.execute(query, (genome_id, ))
    filename = cursor.fetchone()[0]
    return get_accessions_list(filename)

def reference(genome_id, chrom_id, start_position, end_position):
    """Fetch reference sequence of genomic region"""
    db = get_db()
    query = """SELECT filename
               FROM metadata
               WHERE genome=? AND datatype='sequence'"""
    cursor = db.cursor()
    cursor.execute(query, (genome_id, ))
    filename = cursor.fetchone()['filename']
    return get_reference(filename, chrom_id, start_position, end_position)

def two_bit_uri(genome_id):
    db = get_db()
    query = """SELECT filename
               FROM metadata
               WHERE genome=? AND datatype='2bit'"""
    cursor = db.cursor()
    cursor.execute(query, (genome_id, ))
    filename = cursor.fetchone()['filename']
    return filename


def gene_track_uri(genome_id):
    db = get_db()
    query = """SELECT filename
               FROM metadata
               WHERE genome=? AND datatype='bigbed'"""
    cursor = db.cursor()
    cursor.execute(query, (genome_id, ))
    filename = cursor.fetchone()['filename']
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


def haplotypes(genome_id, chrom_id, start_position, end_position, accessions=[]):
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
    variant_file = cursor.fetchone()['filename']

    query = """SELECT filename
            FROM metadata
            WHERE genome=?
            AND datatype='2bit'"""
    cursor = db.cursor()
    cursor.execute(query, (genome_id, ))
    ref_file = cursor.fetchone()['filename']

    haplotypes = get_haplotypes(variant_file, ref_file, chrom_id, start_position, end_position, accessions)

    return haplotypes


def gene_search(genome_id, query):
    raise NotImplementedError()


def feature_search(genome_id, query):
    raise NotImplementedError()
