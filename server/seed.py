#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, User, Search, Comment, Post

def create_users():
    users = []
    usernames = [fake.unique.user_name() for i in range(20)]

    for x in range(20):
        user = User(
            username = usernames[x],
            password_hash = 'password'
        )

        users.append(user)
    
    return users

def create_searches():
    pass

def create_comments():
    pass

def create_posts():
    pass

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print('Clearing db...')
        User.query.delete()
        Search.query.delete()
        Comment.query.delete()
        Post.query.delete()

        print("Seeding users...")
        users = create_users()
        db.session.add_all(users)
        db.session.commit()        
        

