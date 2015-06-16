import os

from flask import Flask

app = Flask(__name__)
config_path = os.environ.get("CONFIG_PATH", "posts.config.DevelopmentConfig")
app.config.from_object(config_path)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

import api
import views
import filters

from database import Base, engine
Base.metadata.create_all(engine)

