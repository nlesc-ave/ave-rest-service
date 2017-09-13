import urllib

from ..db import get_db
from .genomes import get as get_genome


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
    genome_ids = []
    db = get_db()
    query = "SELECT DISTINCT genome FROM metadata WHERE species=?"
    cursor = db.cursor()
    for row in cursor.execute(query, (species_id, )):
        genome_ids.append(row['genome'])

    genome_list = [get_genome(genome_id) for genome_id in genome_ids]
    return genome_list
