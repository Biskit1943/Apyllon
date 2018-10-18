import os

from flasgger import Swagger
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
swagger = Swagger(app, template_file=os.path.join(Config.SWAGGER['doc_dir'], 'template.yml'))


# Get the Version from the Config file
def get_version():
    """Return the VERSION as a string, e.g. for VERSION == (1, 23, 4),
    return '1.23.4'.

    Returns:
        A string representing the Version of this package
    """
    return '.'.join(map(str, Config.VERSION))


__version__ = get_version()


from backend import routes
from backend.database import models