from ..db import get_db


def all():
    """Fetch list of the species with available data."""
    species_list = []
    db = get_db()
    query = "SELECT DISTINCT species FROM metadata"
    cursor = db.cursor()
    for row in cursor.execute(query):
            species_list.append(row['species'])
    return species_list


def genomes(species_id):
    genomes_list = []
    db = get_db()
    query = "SELECT DISTINCT genome FROM metadata WHERE species=?"
    cursor = db.cursor()
    for row in cursor.execute(query, (species_id, )):
        genomes_list.append(row['genome'])
    return genomes_list
