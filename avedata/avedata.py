import os
import connexion
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = connexion.App(__name__, specification_dir='../')
#app.add_api('swagger.yml')


app.app.config.update(dict(
        DATABASE='ave.db'
))
app.app.config.from_pyfile(os.path.join(os.getcwd(),
                           'settings.cfg'), silent=True)


def connect_db():
    """Connects to sqlite database with metadata"""
    rv = sqlite3.connect(app.app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    db = connect_db()
    with app.app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    return db


def get_db():
    """Opens a new database connection if there is none yet for
    the current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        if not os.path.isfile(app.app.config['DATABASE']):
            g.sqlite_db = init_db()
        else:
            g.sqlite_db = connect_db()
    return g.sqlite_db


@app.app.teardown_appcontext
def close_db(error):
    """Closes the database at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
