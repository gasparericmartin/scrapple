#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, User, Search, Comment, Post, user_searches, search_posts

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
    searches = []
    search_terms = ['apple', 'orange', 'banana',
                    'strawberry', 'coconut', 'quince']

    for x in range(20):
        search = Search(
            title = fake.job(),
            search_terms = f'{rc(search_terms)}+{rc(search_terms)}',
            origin_user_id = randint(1, 20)
        )

        searches.append(search)

    return searches

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
        db.session.query(user_searches).delete()
        db.session.query(search_posts).delete()

        print("Seeding users...")
        users = create_users()
        db.session.add_all(users)
        db.session.commit()  

        print('Seeding searches...')
        searches = create_searches()
        db.session.add_all(searches)
        db.session.commit()
        for search in searches: 
            user = User.query.filter_by(id=randint(1,20)).first()
            search.users.append(user)
            db.session.commit()    
        

