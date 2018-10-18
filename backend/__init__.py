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

from backend import routes
from backend.database import models