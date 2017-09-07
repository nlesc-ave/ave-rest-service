import os
from urllib.parse import urlparse

import click
import requests
from flask import current_app
from werkzeug.contrib.profiler import ProfilerMiddleware

from .avedata import connexion_app, app
from .db import get_db, init_db
from .features import features_2_whoosh
from .genes import genes_2_whoosh
from .register import validate_data


@click.group()
def cli():
    pass


@click.command()
@click.option('--debug', help='Enable debug mode', is_flag=True)
@click.option('--profiler', help='Enable profiler mode', is_flag=True)
def run(debug=False, profiler=False):
    """Run web service"""
    if profiler:
        app.config['PROFILE'] = True
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
    connexion_app.run(port=8080, debug=debug)


@click.command()
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
        db = get_db()
        query = """INSERT INTO metadata (species, genome, datatype, filename)
                   VALUES (?,?,?,?)"""
        cursor = db.cursor()
        cursor.execute(query, (species, genome, datatype, filename))
        # commit database updates
        db.commit()
        # if gff file is registered import featur info into features table
        if datatype == "features":
            whoosh_dir = get_woosh_dir(genome + '-features')
            features_2_whoosh(filename, whoosh_dir)
        if datatype == 'genes':
            whoosh_dir = get_woosh_dir(filename)
            genes_2_whoosh(filename, whoosh_dir)

        print("New datafile has been registered.")


def get_woosh_dir(url):
    """
    Based on the bigbed url and base whoosh directory
    from settings generate the path for whoosh directory for index of this bed file
    """
    path = urlparse(url).path
    filename = path.split('/')[-1]
    whoosh_base_dir = current_app.config['WHOOSH_BASE_DIR']
    whoosh_dir = os.path.join(whoosh_base_dir, filename)
    return whoosh_dir


@click.command()
def initdb():
    with app.app_context():
        init_db()


@click.command()
def dropdb():
    click.echo('Dropped the database')


cli.add_command(run)
cli.add_command(register)
cli.add_command(dropdb)
cli.add_command(initdb)
