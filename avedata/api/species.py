from ..db import get_db
import urllib


def all():
    """Fetch list of the species with available data."""
    species_list = []
    db = get_db()
    query = "SELECT DISTINCT species FROM metadata"
    cursor = db.cursor()
    for row in cursor.execute(query):
            name = row['species']
            species_id = urllib.parse.quote(name)
            species_list.append({'name': name, "species_id": species_id})
    return species_list


def genomes(species_id):
    genomes_list = []
    db = get_db()
    query = "SELECT DISTINCT genome FROM metadata WHERE species=?"
    cursor = db.cursor()
    for row in cursor.execute(query, (species_id, )):
        genomes_list.append(row['genome'])
    return genomes_list
