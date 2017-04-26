from ..db import get_db


def search():
    """Fetch list of the species with available data."""
    species_list = []
    db = get_db()
    query = "SELECT DISTINCT species FROM metadata"
    cursor = db.cursor()
    for entry in cursor.execute(query):
            species_list.append(entry['species'])
    return species_list
