#!/usr/bin/env python3

from models import *
from scraper import *
from flask import request, session
from flask_restful import Resource
from config import app, db, api, login_manager
from flask_login import login_required, current_user,login_user ,logout_user
from sqlalchemy import func
import datetime

@login_manager.user_loader
def user_loader(user_id):
    user = User.query.filter_by(id=user_id).first()

    if user:
        return user
    else:
        return

@login_manager.request_loader
def request_loader(request):
    user = User.query.filter_by(id=request.json['id']).first()

    if user:
        return user
    else:
        return

class Home(Resource):
    def get(self):
        return '<h1>Scrapple</h1>'
    
class Signup(Resource):
    def get(self):
        pass

    def post(self):
        check = User.query.filter(func.lower(User.username)
                    == func.lower('JohnDoe')).first()
        
        if not check:
            try:
                new_user = User(
                    username = request.json['username'],
                    password = request.json['password']
                )
                
                db.session.add(new_user)
                db.session.commit()

                return new_user.to_dict(), 201

            except Exception as exc:
                return {'error': f'{exc}'}, 400
        
        return {'error': 'Username already exists'}, 400

class Login(Resource):
    def post(self, id):
        user = User.query.filter_by(id=id).first()

        try:
            if user:
                if user.authenticate(request.json['password']):
                    user.authenticated = True
                    db.session.add(user)
                    db.session.commit()
                    login_user(user, remember=True)

                    return user.to_dict(), 200
        
        except Exception as exc:
            return {'error': exc}, 400

class Logout(Resource):
    @login_required
    def get(self):
        try:
            user = current_user
            user.authenticated = False
            db.session.add(user)
            db.session.commit()
            logout_user()

            return {'message': 'Logout successful'}, 200
        except Exception as exc:
            return {'error': f'{exc}'}, 400
        

class CheckSession(Resource):
    def get(self):
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            return user.to_dict()
        else:
            return {'message': '401: Not Authorized'}, 401

class PostsBySearchId(Resource):
    @login_required
    def get(self, id):
        search = Search.query.filter_by(id=id).first()
        if search:
            posts = [post.to_dict() for post in Search.posts]
            return posts, 200

        return {'errir': '404 not found'}, 404 

api.add_resource(Home, '/')
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login/<int:id>')
api.add_resource(Logout, '/logout')
api.add_resource(PostsBySearchId, '/posts/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
