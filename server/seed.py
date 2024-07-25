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
            password = 'password'
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
    comments = []

    for x in range(20):
        comment = Comment(
            body = fake.paragraph(3, False),
            search_id = randint(1, 20),
            user_id = randint(1, 20)
        )
        comments.append(comment)
    
    return comments

def create_posts():
    posts = []

    for x in range(100):
        post = Post(
            reddit_id = fake.aba(),
            created = fake.date_time_this_decade(),
            title = fake.job(),
            url = fake.url(),
            img_url = fake.image_url(),
            body = fake.paragraph(3, False)
        )
        posts.append(post)

    return posts

def create_search_post_entries():
    searches = Search.query.all()
    posts = Post.query.all()

    for x in range(100):
        rc(searches).posts.append(rc(posts))
        

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
        
        print('Seeding comments...')
        comments = create_comments()
        db.session.add_all(comments)
        db.session.commit()

        print('Seeding posts...')
        posts = create_posts()
        db.session.add_all(posts)
        db.session.commit()

        print('Seeding search_posts...')
        create_search_post_entries()
        db.session.commit()

        print('Seed complete')
        

