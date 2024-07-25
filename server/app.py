#!/usr/bin/env python3

from models import *
from scraper import *
from flask import request, session
from flask_restful import Resource
from config import app, db, api, login_manager
from flask_login import login_required, current_user,login_user ,logout_user
from sqlalchemy import func
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

api.add_resource(Home, '/home')
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/checksession')
api.add_resource(PostsBySearchIds, '/posts')
api.add_resource(Searches, '/searches')
api.add_resource(SearchesByUser, '/searches-by-user')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
