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
        user = User.query.filter_by(username=request.json['username']).first()

        try:
            if user and user.authenticate(request.json['password']):
                login_user(user, remember=True)

                return user.to_dict(), 200
        
        except Exception as exc:
            return {'error': exc}, 400

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
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            return user.to_dict(rules=('-password_hash',))
        else:
            return {'message': '401: Not Authorized'}, 401

class PostsBySearchId(Resource):
    @login_required
    def get(self, id):
        search = Search.query.filter_by(id=id).first()
        if search:
            posts = [post.to_dict() for post in Search.posts]
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
            return {'Error': exc}, 400

api.add_resource(Home, '/home')
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(PostsBySearchId, '/posts/<int:id>')
api.add_resource(Searches, '/searches')
api.add_resource(SearchesByUser, '/searches-by-user')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
