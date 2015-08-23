#import os
from posts import app
from flask.ext.script import Manager
#from flask.ext.migrate import Migrate, MigrateCommand
#from flask.ext.sqlalchemy import SQLAlchemy
#db = SQLAlchemy(app)
#migrate = Migrate(app,db)

#manager.add_command('db', MigrateCommand)

#if __name__ == '__main__':
#    manager.run()
    
from flask.ext.migrate import Migrate, MigrateCommand
from posts.database import Base

class DB(object):
    def __init__(self, metadata):
        self.metadata = metadata

migrate = Migrate(app, DB(Base.metadata))
manager = Manager(app)
manager.add_command('db', MigrateCommand)