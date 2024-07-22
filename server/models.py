from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from config import db

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

user_searches = db.Table('user_searches',
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                        db.Column('search_id', db.Integer, db.ForeignKey('tag.id'))
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

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    #Hash this
    password = db.Column(db.String, nullable=False)

    searches = db.relationship('Search', secondary=user_searches, 
                               back_populates='users', cascade='all, delete-orphan')
    comments = db.relationship('Comment', back_populates='user', cascade='all, delete-orphan')



class Search(db.Model, SerializerMixin):
    __tablename__ = 'searches'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    search_terms = db.Column(db.String, nullable=False)
    
    origin_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    users = db.relationship('User', secondary=user_searches,
                            back_populates='searches', cascade='all, delete-orphan')

    comments = db.relationship('Comment', back_populates='search', cascade='all, delete-orphan')    

class Comment(db.Model, SerializerMixin):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, nullable=False)

    search_id = db.Column(db.Integer, db.ForeignKey('searches.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    search = db.relationship('Search', back_populates='comments')
    user = db.relationship('User', back_populates='comments')




