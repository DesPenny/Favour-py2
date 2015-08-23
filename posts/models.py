from sqlalchemy import Column, Integer, String, Sequence, DateTime
import datetime
from database import Base
from werkzeug.utils import secure_filename
from flask.ext.login import UserMixin

class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    email = Column(String(128), unique=True)
    password = Column(String(128))
    
    def as_dictionary(self):
        user = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password":self.password
            
        }
        return user
    
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    body = Column(String(1024))
    #datetime = Column(DateTime, default=datetime.datetime.now)
    
    def as_dictionary(self):
        post = {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            #"datetime":self.datetime
            
        }
        return post
    
    def main_image(self):
        return secure_filename(str(self.id))
        