"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

default_image_url = "https://img.freepik.com/free-vector/user-blue-gradient_78370-4692.jpg?w=826&t=st=1712240115~exp=1712240715~hmac=ec275943900481bfc64f790c547f043f8554bf3398e6cf2fab36de9dc3f590ce"

def connect_db(app):
     db.app = app
     db.init_app(app)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.Text,
                           nullable=False,)
    
    last_name = db.Column(db.Text,
                          nullable=False)
    
    image_url = db.Column(db.Text,
                          nullable=False,
                          default=default_image_url)
    
    posts = db.relationship("Post", backref="user", )
    
    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    title = db.Column(db.Text,
                      nullable=False)
    
    content = db.Column(db.Text,
                        nullable=False)
    
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.now)
    
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id'), 
                        nullable=False)

class PostTag(db.Model):
    """Tags on a post."""

    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

class Tag(db.Model):
    """A tag that can be added to a post."""
    __tablename__ = "tags"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    tag_name = db.Column(db.Text,
                        unique=True)
    
    posts = db.relationship('Post', secondary="post_tags", backref="tags")

