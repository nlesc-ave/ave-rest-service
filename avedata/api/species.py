import urllib

from ..db import species_names, genomes_of_species
from .genomes import get as get_genome


def search():
    """Fetch list of the species with available data."""
    species_list = []
    for name in species_names():
        species_id = urllib.parse.quote(name)
        species_list.append({'name': name, "species_id": species_id})
    return species_list


def genomes(species_id):
    genome_ids = genomes_of_species(species_id)
    genome_list = [get_genome(genome_id) for genome_id in genome_ids]
    return genome_list
