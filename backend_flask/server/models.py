from . import db, jwt
from flask_login import UserMixin
from sqlalchemy.sql import func
from uuid import uuid4

def get_uuid():
    return uuid4().hex

class User(db.Model, UserMixin):
    id = db.Column(db.String(100), unique=True, primary_key=True, default=get_uuid)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150), unique=True)
