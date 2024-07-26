from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
import os
import hashlib
from config import db, login_manager

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

    serialize_rules = (
        '-searches.posts',
    )

    id = db.Column(db.Integer, primary_key=True)
    reddit_id = db.Column(db.String, nullable=False, unique=True)
    created = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String)
    body = db.Column(db.String)

    searches = db.relationship('Search', secondary=search_posts, back_populates='posts')

    def __repr__(self):
        return f'<ID:{self.id}, REDDIT_ID:{self.reddit_id}, TITLE:{self.title}>'

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = (
        '-password_hash', 
        '-searches.users', 
        '-searches.comments',
        '' 
        '-comments.user', 
        '-comments.search')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)

    #Add created searches relationship using search property origin_user_id
    searches = db.relationship('Search', secondary=user_searches, back_populates='users')
    comments = db.relationship('Comment', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<ID:{self.id}, USERNAME:{self.username}>'

    @hybrid_property
    def password(self):
        return self.password_hash
    
    @password.setter
    def password(self, password):
        salt = os.urandom(16)

        hash_value = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            10000
        )

        self.password_hash = salt + hash_value
    
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
    
    def is_active(self):
        return True
    
    def get_id(self):
        return self.id
    
    def is_authenticated(self):
        return self.authenticated
    
    def is_anonymous(self):
        return False


class Search(db.Model, SerializerMixin):
    __tablename__ = 'searches'

    serialize_rules = (
        '-users.searches',
        '-comments.search',
        '-posts.searches'
        )

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    search_terms = db.Column(db.String, nullable=False)
    
    origin_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    users = db.relationship('User', secondary=user_searches, back_populates='searches')
    comments = db.relationship('Comment', back_populates='search', cascade='all, delete-orphan')
    posts = db.relationship('Post', secondary=search_posts, back_populates='searches') 

    def __repr__(self):
        return f'ID:{self.id}, TITLE:{self.title}, SEARCH_TERMS:{self.search_terms}'   

class Comment(db.Model, SerializerMixin):
    __tablename__ = 'comments'

    serialize_rules = (
        '-search.comments',
        '-user.comments',
        '-user.searches.comments'
    )

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, nullable=False)

    search_id = db.Column(db.Integer, db.ForeignKey('searches.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    search = db.relationship('Search', back_populates='comments')
    user = db.relationship('User', back_populates='comments')

    def __repr__(self):
        return f'ID:{self.id}, BODY:{self.body[:15]}'



