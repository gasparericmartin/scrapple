from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
import os
import hashlib
from config import db, metadata

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

user_searches = db.Table('user_searches',
                        db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                        db.Column('search_id', db.Integer, db.ForeignKey('searches.id'))
                        )

search_posts = db.Table('search_posts',
                        db.Column('search_id', db.Integer, db.ForeignKey('searches.id')),
                        db.Column('post_id', db.Integer, db.ForeignKey('posts.id'))
                        )

class Post(db.Model, SerializerMixin):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    reddit_id = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String)
    body = db.Column(db.String)

    searches = db.relationship('Search', secondary=search_posts, back_populates='posts')

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    _password_hash = db.Column(db.String(128), nullable=False)

    searches = db.relationship('Search', secondary=user_searches, back_populates='users')
    comments = db.relationship('Comment', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        pass

    @hybrid_property
    def password_hash(self):
        return self._password_hash
    
    @password_hash.setter
    def password_hash(self, password):
        salt = os.urandom(16)

        hash_value = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            10000
        )

        self._password_hash = salt + hash_value
    
    def authenticate(self, password):
        salt = self.password_hash[:16]
        key = self.password_hash[16:]

        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            10000
        )
    
        if password_hash == key:
            return True
        else:
            return False


class Search(db.Model, SerializerMixin):
    __tablename__ = 'searches'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    search_terms = db.Column(db.String, nullable=False)
    
    origin_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    users = db.relationship('User', secondary=user_searches,back_populates='searches')
    comments = db.relationship('Comment', back_populates='search', cascade='all, delete-orphan')
    posts = db.relationship('Post', secondary=search_posts, back_populates='searches')    

class Comment(db.Model, SerializerMixin):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, nullable=False)

    search_id = db.Column(db.Integer, db.ForeignKey('searches.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    search = db.relationship('Search', back_populates='comments')
    user = db.relationship('User', back_populates='comments')




