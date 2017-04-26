from flask import current_app, g
import sqlite3
import os


def connect_db():
    """Connects to sqlite database with metadata"""
    rv = sqlite3.connect(current_app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    db = connect_db()
    with current_app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    return db


def get_db():
    """Opens a new database connection if there is none yet for
    the current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        if not os.path.isfile(current_app.config['DATABASE']):
            g.sqlite_db = init_db()
        else:
            g.sqlite_db = connect_db()
    return g.sqlite_db


# @current_app.teardown_appcontext
# def close_db(error):
#     """Closes the database at the end of the request."""
#     if hasattr(g, 'sqlite_db'):
#         g.sqlite_db.close()
