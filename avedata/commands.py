import click
import os
from .db import get_db, init_db
from .avedata import connexion_app, app
from connexion.resolver import RestyResolver
from .register import validate_data, import_gff


@click.group()
def cli():
    pass


@click.command()
def run():
    """Run web service"""
    connexion_app.add_api('swagger.yml', arguments=app.config)
    connexion_app.run(port=8080, debug=True)


@click.command()
@click.option('--species', help='Species name')
@click.option('--genome', help='Name of the reference genome')
@click.option('--datatype', help='Type of the data',
              type=click.Choice(['sequence', 'features', 'variants',
                                 '2bit', 'bigbed']))
@click.argument('filename')
def register(species, genome, datatype, filename):
    """Add file metadata iformation to the database"""
    # check if file exists
    file_abs_path = os.path.join(os.getcwd(), filename)
    if not os.path.isfile(file_abs_path):
        try:
            requests.head(filename)
            print("File %s is not available" % click.format_filename(filename))
        except requests.HTTPError:
            print("URL %s is not available" % click.format_filename(filename))
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
