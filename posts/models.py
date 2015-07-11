from sqlalchemy import Column, Integer, String, Sequence, DateTime
import datetime
from database import Base
from werkzeug.utils import secure_filename

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