import click
import os
from .avedata import get_db, app
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
    if not os.path.isfile(os.path.join(os.getcwd(), filename)):
        print("File %s does not exist" % click.format_filename(filename))
        return

    with app.app.app_context():
        db = get_db()
        query = 'INSERT INTO metadata (species, genome, datatype, filename) VALUES (?,?,?,?)'
        db.cursor().execute(query, (species, genome, datatype, filename))
        db.commit()
        print("New datafile has been registered.")

@click.command()
def dropdb():
    click.echo('Dropped the database')


cli.add_command(run)
cli.add_command(register)
cli.add_command(dropdb)


