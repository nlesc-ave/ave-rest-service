import click
from .avedata import init_db, app

@click.group()
def cli():
    pass

@click.command()
def run():
    app.run(port=8080, debug=True)

@click.command()
def initdb():
    with app.app.app_context():
        init_db()
        click.echo('Initialized the database')

@click.command()
def dropdb():
    click.echo('Dropped the database')

cli.add_command(run)
cli.add_command(initdb)
cli.add_command(dropdb)

