from . import db, jwt
from flask_login import UserMixin
from sqlalchemy.sql import func
from uuid import uuid4
import json

def get_uuid():
    return uuid4().hex

class User(db.Model, UserMixin):
    id = db.Column(db.String(100), unique=True, primary_key=True, default=get_uuid)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150), unique=True)
    favorites = db.relationship('Favorite')

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10000))
    user_id = db.Column(db.String, db.ForeignKey('user.id'))