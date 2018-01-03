import os
from shutil import rmtree

import click
from flask import current_app
from werkzeug.contrib.profiler import ProfilerMiddleware

from .app import connexion_app, app
from .db import genome_of_filename, init_db, insert_file, delete_file, all_metas, is_genes, is_features
from .features import features_2_whoosh, featurebb2label, drop_track
from .genes import genes_2_whoosh
from .register import validate_data
from .version import __version__
from .whoosh import get_woosh_dir


@click.group()
@click.version_option(__version__)
def cli():
    pass


@cli.command()
@click.option('--port', '-p', help='TCP port to bind to', default=8080)
@click.option('--debug', help='Enable debug mode', is_flag=True)
@click.option('--profiler', help='Enable profiler mode', is_flag=True)
def run(port, debug=False, profiler=False):
    """Run as single threaded web service, for development only, use gunicorn in production"""
    if profiler:
        app.config['PROFILE'] = True
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
    connexion_app.run(port=port, debug=debug)


@cli.command()
@click.option('--species', help='Species name')
@click.option('--genome', help='Name of the reference genome')
@click.option('--datatype', help='Type of the data',
              type=click.Choice(['features', 'variants', '2bit', 'genes']))
@click.argument('filename')
def register(species, genome, datatype, filename):
    """Add file metadata information to the database"""
    # validate if the provided files can be accessed
    # by relevant libraries
    validate_data(filename, datatype)

    with app.app_context():
        register_file(datatype, filename, genome, species)
        click.echo("New datafile has been registered.")


def register_file(datatype, filename, genome, species):
    insert_file(datatype, filename, genome, species)
    # if gff file is registered import featur info into features table
    whoosh_base_dir = current_app.config['WHOOSH_BASE_DIR']
    if datatype == "features":
        whoosh_dir = get_woosh_dir(genome + '-features', whoosh_base_dir)
        features_2_whoosh(filename, whoosh_dir)
    if datatype == 'genes':
        whoosh_dir = get_woosh_dir(filename, whoosh_base_dir)
        genes_2_whoosh(filename, whoosh_dir)


@cli.command()
def list():
    """List of registered files/urls in the database"""
    with app.app_context():
        print("species\tgenome\tdatatype\tfilename")
        for row in all_metas():
            print("\t".join(row))


@cli.command()
@click.argument('filename')
def deregister(filename):
    """Remove a filename or url from the database"""
    with app.app_context():
        whoosh_base_dir = current_app.config['WHOOSH_BASE_DIR']
        if is_genes(filename):
            whoosh_dir = get_woosh_dir(filename, whoosh_base_dir)
            rmtree(whoosh_dir)
        elif is_features(filename):
            genome = genome_of_filename(filename)
            whoosh_dir = get_woosh_dir(genome + '-features', whoosh_base_dir)
            track = featurebb2label(filename)
            drop_track(track, whoosh_dir)
        delete_file(filename)
        click.echo("Deregistered entry")


@cli.command()
def init_db():
    """Initializes database"""
    with app.app_context():
        init_db()
        click.echo("Database initialized")


@cli.command()
def drop_db():
    """Drops database"""
    with app.app_context():
        dbfn = current_app.config['DATABASE']
        os.remove(dbfn)
        click.echo("Database removed")
