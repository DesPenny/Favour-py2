import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)


config_path = os.environ.get("CONFIG_PATH", "posts.config.DevelopmentConfig")
app.config.from_object(config_path)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

db = SQLAlchemy(app)

import models
import api
import views
import filters
import login

from database import Base, engine
Base.metadata.create_all(engine)

