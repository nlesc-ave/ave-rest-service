import connexion
from flask import current_app, Response
import simplejson

from ..db import genome_filename, variants_filename, feature_urls, gene_url, species_of_genome
from ..features import featurebb2label, find_features
from ..genes import find_genes
from ..sequence import get_chrominfo, InvalidChromosome
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
            'reference': genome_filename(genome_id),
            'species': species_of_genome(genome_id)
        }
        try:
            genome_info['variants_filename'] = variants_filename(genome_id)
        except LookupError:
            # variants_filename is optional
            pass
        try:
            genome_info['gene_track'] = gene_url(genome_id)
        except LookupError:
            # gene_track is optional
            pass

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
    filename = genome_filename(genome_id)
    return get_chrominfo(filename)


def feature_tracks(genome_id):
    tracks = []
    for url in feature_urls(genome_id):
        label = featurebb2label(url)
        track = {
            'label': label,
            'url': url
        }
        tracks.append(track)
    return tracks


def accession_list(genome_id):
    filename = variants_filename(genome_id)
    return get_accessions_list(filename)


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

    # to construct haplotypes, both:
    # variants from bcf file and
    # reference sequence from 2bit
    # are needed
    try:
        variant_file = variants_filename(genome_id)
    except LookupError:
        ext = {'genome_id': genome_id}
        message = "Genome with id \'{0}\' contains no variants".format(genome_id)
        return connexion.problem(404, "Not Found", message, ext=ext)

    try:
        ref_file = genome_filename(genome_id)
    except LookupError:
        ext = {'genome_id': genome_id}
        message = "Genome with id \'{0}\' not found".format(genome_id)
        return connexion.problem(404, "Not Found", message, ext=ext)

    if accessions is None:
        accessions = []

    try:
        res = get_haplotypes(variant_file, ref_file, chrom_id, start_position, end_position, accessions)
        return Response(simplejson.dumps(res), status=200, mimetype='application/json')
    except AccessionsLookupError as e:
        ext = {'genome_id': genome_id, 'accessions': list(e.accessions)}
        return connexion.problem(404, "Not Found", "Some accessions not found", ext=ext)
    except InvalidChromosome:
        ext = {'genome_id': genome_id, 'chrom_id': chrom_id}
        msg = "Chromosome '{chrom_id}' no found in '{genome_id}' genome".format(**ext)
        return connexion.problem(404, "Not Found", msg, ext=ext)


def gene_search(genome_id, query):
    try:
        genes_file = gene_url(genome_id)
    except LookupError:
        ext = {'genome_id': genome_id}
        return connexion.problem(404, "Not Found", "Genes for genome with id \'{0}\' not found".format(genome_id), ext=ext)

    # then we'll find out what is the whoosh path for index of this bigbed file
    whoosh_base_dir = current_app.config['WHOOSH_BASE_DIR']
    whoosh_dir = get_woosh_dir(genes_file, whoosh_base_dir)
    return find_genes(whoosh_dir, query)


def feature_search(genome_id, query):
    if not feature_urls(genome_id):
        ext = {'genome_id': genome_id}
        return connexion.problem(404, "Not Found", "Features for genome with id \'{0}\' not found".format(genome_id), ext=ext)

    whoosh_base_dir = current_app.config['WHOOSH_BASE_DIR']
    whoosh_dir = get_woosh_dir(genome_id + '-features', whoosh_base_dir)
    return find_features(whoosh_dir, query)
