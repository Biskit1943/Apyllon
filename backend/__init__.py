import os

from flasgger import Swagger
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)

db = SQLAlchemy(app, session_options={"autoflush": True})
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

# Prevent circular imports
from backend.database import models
#db.create_all()
from backend import routes
