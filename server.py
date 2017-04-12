import os
import connexion
import sqlite3

app = connexion.App(__name__, specification_dir='./')
app.add_api('swagger.yml')
app.run(port=8080)


app.config.update(dict(
        DATABASE=os.path.join(app.root_path, 'db', 'sqlite', 'ave.db')
))


def connect_db():
    """Connects to sqlite database with metadata"""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

