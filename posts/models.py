from sqlalchemy import Column, Integer, String, Sequence, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
import datetime
from database import Base
from .database import session
from werkzeug.utils import secure_filename
from flask.ext.login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    email = Column(String(128), unique=True)
    password = Column(String(128))
    posts = relationship("Post", backref="author")
    confirmed = Column(Boolean, default=False)
    
    
    def as_dictionary(self):
        user = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password":self.password,
            "confirmed":self.confirmed
            
        }
        return user
    
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer('somesecretkey', expiration)
        return s.dumps({'confirm':self.id})
        
    def confirm(self,token):
        s = Serializer('somesecretkey')
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        session.add(self)
        return True
    
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    body = Column(String(1024))
    datetime = Column(DateTime, default=datetime.datetime.now)
    author_id = Column(Integer, ForeignKey('users.id'))
    
    def as_dictionary(self):
        post = {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "datetime":self.datetime,
            "author_id":self.author_id
            
        }
        return post
    
    def main_image(self):
        return secure_filename(str(self.id))
        