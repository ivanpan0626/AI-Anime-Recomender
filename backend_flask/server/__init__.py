from flask import Flask
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from os import path

db = SQLAlchemy()
jwt = JWTManager()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:3000"}})
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    app.config['JWT_COOKIE_SAMESITE'] = 'None'
    app.config["JWT_COOKIE_SECURE"] = True
    app.config["JWT_SECRET_KEY"] = "sasdasdsadsadasd"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    db.init_app(app)
    jwt.init_app(app)

    from .auth import auth
    from .anime import anime
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(anime, url_prefix='/')

    with app.app_context():
        db.create_all()

    return app

def create_database(app):
    if not path.exists('server/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')