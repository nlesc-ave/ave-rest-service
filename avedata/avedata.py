import os
from urllib.parse import urlparse

import connexion
from flask_cors import CORS

from .version import __version__

connexion_app = connexion.FlaskApp(__name__, specification_dir='../')
app = connexion_app.app
CORS(app)

app.config.update(dict(
    # File path for database
    DATABASE='ave.db',
    # Maximum number of base pairs at which haplotype clustering is performed
    MAX_RANGE=50000,
    # Directory to store whoosh full text indices
    WHOOSH_BASE_DIR='.',
))
app.config.from_pyfile(os.path.join(os.getcwd(), 'settings.cfg'), silent=True)


def spec_config():
    url = os.environ.get('EXTERNAL_URL', app.config.get('EXTERNAL_URL', None))
    conf = {'VERSION': __version__}
    if url:
        o = urlparse(url)
        conf['HOSTPORT'] = o.netloc
        conf['SCHEME'] = o.scheme
    return conf


connexion_app.add_api('swagger.yml', arguments=spec_config())
