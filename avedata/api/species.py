

from ..db import genomes_of_species, all_species
from .genomes import get as get_genome


def search():
    """Fetch list of the species with available data."""
    return all_species()


def genomes(species_id):
    genome_ids = genomes_of_species(species_id)
    genome_list = [get_genome(genome_id) for genome_id in genome_ids]
    return genome_list
