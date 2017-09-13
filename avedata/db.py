import sqlite3
import os

from pkg_resources import resource_string
from flask import current_app, g


def connect_db():
    """Connects to sqlite database with metadata"""
    rv = sqlite3.connect(current_app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    db = connect_db()
    sql = resource_string(__name__, 'schema.sql').decode('utf8')
    db.cursor().executescript(sql)
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
