#!/usr/bin/env python3

from models import *
from scraper import *
from flask import request, session
from flask_restful import Resource
from config import app, db, api
from sqlalchemy import func
import datetime

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
        
        return {'error': 'Username already exists'}

class Login(Resource):
    def get(self):
        pass

    def post(self):
        pass

class CheckSession(Resource):
    def get(self):
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            return user.to_dict()
        else:
            return {'message': '401: Not Authorized'}, 401

class PostsBySearchId(Resource):
    def get(self, id):
        search = Search.query.filter_by(id=id).first()
        if search:
            posts = [post.to_dict() for post in Search.posts]
            return posts, 200

        return {'errir': '404 not found'}, 404 

api.add_resource(Home, '/')
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(PostsBySearchId, '/posts/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
