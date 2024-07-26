#!/usr/bin/env python3

from models import *
from scraper import scrape, get_data
from flask import request, session
from flask_restful import Resource
from config import app, db, api, login_manager
from flask_login import login_required, current_user,login_user ,logout_user
from sqlalchemy import func
from dateutil.parser import *
import datetime
import sys

@login_manager.user_loader
def user_loader(user_id):
    user = User.query.filter_by(id=user_id).first()

    if user:
        return user
    else:
        return

class Home(Resource):
    @login_required
    def get(self):
        return '<h1>Scrapple</h1>'
    
class Signup(Resource):
    def get(self):
        pass

    def post(self):
        check = User.query.filter(func.lower(User.username)
                    == func.lower(request.json['username'])).first()
        
        if not check:
            try:
                new_user = User(
                    username = request.json['username'],
                    password = request.json['password']
                )
                
                db.session.add(new_user)
                db.session.commit()

                return new_user.to_dict(rules=('-password_hash',)), 201

            except Exception as exc:
                return {'error': f'{exc}'}, 400
        
        return {'error': 'Username already exists'}, 400

class Login(Resource):
    def post(self):
        user = User.query.filter(func.lower(User.username)
                    == func.lower(request.json['username'])).first()
        authenticated = False
        logged_in = isinstance(current_user._get_current_object(), User)

        if user:
            authenticated = user.authenticate(request.json['password'])

        try:
            if not user:
                return {'error': 'User not found'}, 404
                  
            elif user and authenticated and not logged_in:
                login_user(user, remember=True)

                return user.to_dict(), 200
            
            elif logged_in and current_user.id == user.id:
                
                return {'error': 'Already logged in'}, 400
            
            else:

                return {'error': 'Not logged in'}, 400
            
        except Exception as exc:
            return {'error': f'{exc}'}, 400

class Logout(Resource):
    @login_required
    def get(self):
        try:
            logout_user()

            return {'message': 'Logout successful'}, 200
        
        except Exception as exc:
            return {'error': f'{exc}'}, 400
        

class CheckSession(Resource):
    def get(self):
        if isinstance(current_user._get_current_object(), User):
            return current_user.to_dict(), 200
        else:
            return {'message': '401: Not Authorized'}, 401

class PostsBySearchIds(Resource):
    @login_required
    def get(self):
        ##Avoid this complexity by creating Post-User relationship
        #through Search
        # search_ids = [id for id in request.json['searchids']]
        search_ids = [search.id for search in current_user.searches]
        searches = [Search.query.filter_by(id=search_id).first() for search_id in search_ids]
        
        if searches:
            posts = []
            for search in searches:
                [posts.append(post.to_dict()) for post in search.posts if post.to_dict() not in posts]

            return posts, 200

        return {'error': '404 not found'}, 404

class Searches (Resource):
    @login_required
    def get(self):
        searches = Search.query.all()

        if searches:
            searches_dict = [search.to_dict() for search in searches]
            return searches_dict, 200
        
        return {'Error': '404 not found'}, 404
    
    @login_required
    def post(self):
        user = User.query.filter_by(id=request.json['user_id']).first()
        try:
            new_search = Search(
                title = request.json['title'],
                search_terms = request.json['search_terms'],
                origin_user_id = request.json['user_id']
            )

            db.session.add(new_search)
            db.session.commit()

            new_search.users.append(user)
            db.session.commit()

            return new_search.to_dict(), 201
        
        except Exception as exc:
            return {'error': f'{exc}'}, 400

class SearchesByUser(Resource):
    @login_required
    def get(self):
        searches = [search.to_dict() for search in current_user.searches]

        try:
            if searches:
                return searches, 200
            return {'Error': 'No searches found'}, 404
        except Exception as exc:
            return {'Error': f'{exc}'}, 400

class Comments(Resource):
    @login_required
    def post(self):

        try:
            new_comment = Comment(
                body = request.json['body'],
                search_id = request.json['search_id'],
                user_id = current_user.id
            )

            db.session.add(new_comment)
            db.session.commit()

            return new_comment.to_dict(), 201
        
        except Exception as exc:
            pass

class Scrape(Resource):
    @login_required
    def post(self):
        
        search = Search.query.filter_by(id=request.json['search_id']).first()
        raw_posts = scrape(
            search_terms = request.json['search_terms'],
            limit = request.json['limit'],
            reddit_id = request.json['reddit_id'],
            before_after = request.json['before_after']
        )
        new_posts = []
        
        if raw_posts:
            for post in raw_posts:
                if not Post.query.filter_by(reddit_id=post['full_name']).first():
                    new_post = Post(
                    reddit_id = post['full_name'],
                    created = parse(post['date_time']),
                    title = post['post_title'],
                    url = post['post_link'],
                    img_url = post['post_img'],
                    body = post['post_body']  
                    )
                    new_posts.append(new_post)
                
            db.session.add_all(new_posts)
            db.session.commit()
            
            search.posts.extend(new_posts)
            db.session.commit()
            
            new_posts_dict = [post.to_dict() for post in new_posts]
     
            
            if len(new_posts_dict) == 0:
                return {'message': 'No new posts'}, 204
            
            return {'posts': new_posts_dict, 'search': search.to_dict()}, 200    
    


api.add_resource(Home, '/home')
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/checksession')
api.add_resource(PostsBySearchIds, '/posts')
api.add_resource(Searches, '/searches')
api.add_resource(SearchesByUser, '/searches-by-user')
api.add_resource(Comments, '/comments')
api.add_resource(Scrape, '/scrape')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
