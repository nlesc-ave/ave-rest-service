import os

import click
import requests
from werkzeug.contrib.profiler import ProfilerMiddleware

from .db import get_db, init_db
from .avedata import connexion_app, app
from .register import validate_data, import_gff
from .genes import big_bed_2_whoosh

from urllib.parse import urlparse
from flask import current_app

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
    connexion_app.add_api('swagger.yml', arguments=app.config)
    connexion_app.run(port=8080, debug=debug)


@click.command()
@click.option('--species', help='Species name')
@click.option('--genome', help='Name of the reference genome')
@click.option('--datatype', help='Type of the data',
              type=click.Choice(['features', 'variants', '2bit', 'bigbed']))
@click.argument('filename')
def register(species, genome, datatype, filename):
    """Add file metadata information to the database"""
    # check if file exists
    file_abs_path = os.path.join(os.getcwd(), filename)
    if not os.path.isfile(file_abs_path):
        try:
            s = requests.Session()
            s.head(filename)
        except requests.HTTPError:
            print("file or URL %s is not available" %
                  click.format_filename(filename))
            return

    # validate if the provided files can be accessed
    # by relevant libraries
    validate_data(file_abs_path, datatype)

    with app.app_context():
        db = get_db()
        query = """INSERT INTO metadata (species, genome, datatype, filename)
                   VALUES (?,?,?,?)"""
        cursor = db.cursor()
        cursor.execute(query, (species, genome, datatype, filename))
        meta_id = cursor.lastrowid
        # commit database updates
        db.commit()
        # if gff file is registered import featur info into features table
        if datatype == "features":
            import_gff(db, meta_id, filename)
        if datatype == 'bigbed':
            whoosh_dir = get_woosh_dir(filename)
            big_bed_2_whoosh(filename, whoosh_dir)

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
