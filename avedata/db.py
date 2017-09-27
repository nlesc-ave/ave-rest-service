import sqlite3
import os
import urllib

from pkg_resources import resource_string
from flask import current_app, g


def connect_db():
    """Connects to sqlite database with metadata"""
    rv = sqlite3.connect(current_app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    db = connect_db()
    sql = resource_string(__name__, 'schema.sql').decode('utf8')
    db.cursor().executescript(sql)
    db.commit()
    return db


def get_db():
    """Opens a new database connection if there is none yet for
    the current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        if not os.path.isfile(current_app.config['DATABASE']):
            g.sqlite_db = init_db()
        else:
            g.sqlite_db = connect_db()
    return g.sqlite_db


def insert_file(datatype, filename, genome, species):
    db = get_db()
    query = """INSERT INTO metadata (species, genome, datatype, filename)
                       VALUES (?,?,?,?)"""
    cursor = db.cursor()
    cursor.execute(query, (species, genome, datatype, filename))
    db.commit()


def delete_file(filename):
    db = get_db()
    c = db.cursor()
    sql = 'DELETE FROM metadata WHERE filename=?'
    c.execute(sql, (filename,))
    db.commit()


def all_metas():
    db = get_db()
    c = db.cursor()
    sql = 'SELECT species, genome, datatype, filename FROM metadata'
    return c.execute(sql)


def is_datatype(filename, datatype):
    db = get_db()
    c = db.cursor()
    sql = 'SELECT 1 FROM metadata WHERE filename=? AND datatype=?'
    c.execute(sql, (filename, datatype))
    row = c.fetchone()
    return row is not None


def is_genes(filename):
    return is_datatype(filename, 'genes')


def is_features(filename):
    return is_datatype(filename, 'features')


def genome_of_filename(filename):
    db = get_db()
    c = db.cursor()
    sql = 'SELECT genome FROM metadata WHERE filename=?'
    c.execute(sql, (filename, ))
    return c.fetchone()[0]


def get_filename(genome_id, datatype):
    db = get_db()
    query = 'SELECT filename FROM metadata WHERE genome=? AND datatype=?'
    cursor = db.cursor()
    cursor.execute(query, (genome_id, datatype,))
    result = cursor.fetchone()
    if result is None:
        raise LookupError()
    return result[0]


def genome_filename(genome_id):
    return get_filename(genome_id, '2bit')


def variants_filename(genome_id):
    return get_filename(genome_id, 'variants')


def feature_urls(genome_id):
    db = get_db()
    query = """SELECT filename
                   FROM metadata
                   WHERE genome=? AND datatype='features'"""
    cursor = db.cursor()
    urls = []
    for row in cursor.execute(query, (genome_id,)):
        urls.append(row[0])
    return urls


def gene_url(genome_id):
    return get_filename(genome_id, 'genes')


def species_names():
    db = get_db()
    query = "SELECT DISTINCT species FROM metadata"
    cursor = db.cursor()
    names = []
    for row in cursor.execute(query):
        names.append(row[0])
    return names


def genomes_of_species(species_id):
    genome_ids = []
    db = get_db()
    query = "SELECT DISTINCT genome FROM metadata WHERE species=?"
    cursor = db.cursor()
    for row in cursor.execute(query, (species_id, )):
        genome_ids.append(row['genome'])
    return genome_ids


def build_species(name):
    species_id = urllib.parse.quote(name)
    return {'name': name, "species_id": species_id}


def all_species():
    species_list = []
    for name in species_names():
        species_list.append(build_species(name))
    return species_list


def species_of_genome(genome_id):
    db = get_db()
    query = "SELECT species FROM metadata WHERE genome=? AND datatype='2bit'"
    cursor = db.cursor()
    cursor.execute(query, (genome_id, ))
    result = cursor.fetchone()
    if result is None:
        raise LookupError()
    return build_species(result[0])
