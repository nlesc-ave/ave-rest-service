import click
from flask import current_app
from werkzeug.contrib.profiler import ProfilerMiddleware

from .app import connexion_app, app
from .db import get_db, init_db
from .features import features_2_whoosh
from .genes import genes_2_whoosh
from .register import validate_data
from .version import __version__
from .whoosh import get_woosh_dir


@click.group()
@click.version_option(__version__)
def cli():
    pass


@click.command()
@click.option('--port', '-p', help='TCP port to bind to', default=8080)
@click.option('--debug', help='Enable debug mode', is_flag=True)
@click.option('--profiler', help='Enable profiler mode', is_flag=True)
def run(port, debug=False, profiler=False):
    """Run web service"""
    if profiler:
        app.config['PROFILE'] = True
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
    connexion_app.run(port=port, debug=debug)


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
        whoosh_base_dir = current_app.config['WHOOSH_BASE_DIR']
        if datatype == "features":
            whoosh_dir = get_woosh_dir(genome + '-features', whoosh_base_dir)
            features_2_whoosh(filename, whoosh_dir)
        if datatype == 'genes':
            whoosh_dir = get_woosh_dir(filename, whoosh_base_dir)
            genes_2_whoosh(filename, whoosh_dir)

        print("New datafile has been registered.")


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
