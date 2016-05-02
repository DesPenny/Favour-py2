import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask.ext.mail import Mail

mail = Mail()

app = Flask(__name__)
Bootstrap(app)
mail.init_app(app)

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

