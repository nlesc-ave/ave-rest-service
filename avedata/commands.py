import click
import os
from .avedata import get_db, app
from .db import validate_data, import_gff
from flask import current_app


@click.group()
def cli():
    pass


@click.command()
def run():
    """Run web service"""
    app.run(port=8080, debug=True)


@click.command()
@click.option('--species', help='Species name')
@click.option('--genome', help='Name of the reference genome')
@click.option('--datatype', help='Type of the data',
              type=click.Choice(['sequence', 'features', 'variants']))
@click.argument('filename')
def register(species, genome, datatype, filename):
    """Add file metadata iformation to the database"""
    # check if file exists
    file_abs_path = os.path.join(os.getcwd(), filename)
    if not os.path.isfile(file_abs_path):
        print("File %s does not exist" % click.format_filename(filename))
        return

    # validate if the provided files can be accessed
    # by relevant libraries
    validate_data(file_abs_path, datatype)

    with app.app.app_context():
        db = get_db()
        query = """INSERT INTO metadata (species, genome, datatype, filename)
                   VALUES (?,?,?,?)"""
        db.cursor().execute(query, (species, genome, datatype, filename))
        meta_id = db.cursor().lastrowid
        # commit database updates
        db.commit()
        # if gff file is registered import featur info into features table

        import_gff(db, meta_id, rowfilename)


        print("New datafile has been registered.")


@click.command()
def dropdb():
    click.echo('Dropped the database')


cli.add_command(run)
cli.add_command(register)
cli.add_command(dropdb)
