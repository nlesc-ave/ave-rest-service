import os
import connexion
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from flask_cors import CORS

connexion_app = connexion.App(__name__, specification_dir='../')
app = connexion_app.app
CORS(app)

app.config.update(dict(
    DATABASE='ave.db'
))
app.config.from_pyfile(os.path.join(os.getcwd(),
                                    'settings.cfg'), silent=True)
