#!/usr/bin/env python3

from models import *
from flask import request
from flask_restful import Resource
from config import app, db, api
from flask import request
import datetime

class Home(Resource):
    def get(self):
        return '<h1>Scrapple</h1>'


api.add_resource(Home, '/')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
