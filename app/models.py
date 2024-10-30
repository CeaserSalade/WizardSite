from . import db
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from datetime import datetime

bcrypt = Bcrypt()

# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


# Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(280), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    like_count = db.Column(db.Integer, default=0)
    topics = db.Column(db.String(200))

    # Relationship with Comment
    comments = db.relationship('Comment', backref='post', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Post {self.id} by {self.username}>'


# Comment model
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(280), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    like_count = db.Column(db.Integer, default=0)
