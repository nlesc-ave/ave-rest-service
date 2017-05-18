from ..db import get_db
from ..sequence import get_chrominfo
from ..sequence import get_reference
from ..features import get_genes
from ..features import get_annotations

def chromosomes(genome_id):
    """Fetch fasta file name for this genome
        open file with pyfaidx
        get list of chromosomes and fetch their 'chrom_id': len
        retun [{'chrom_id': lenght},]
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
    return get_genes(filename, genome_id, chrom_id, start_position, end_position)


def annotations(genome_id):
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
    return get_annotations(filename)
