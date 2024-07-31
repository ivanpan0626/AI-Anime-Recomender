from flask import request, jsonify, redirect, Blueprint, make_response
from . import db, jwt
from .models import User, Favorite
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required, current_user, unset_jwt_cookies, set_access_cookies
from werkzeug.security import generate_password_hash, check_password_hash

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()

auth = Blueprint('auth', __name__)

@auth.route("/signup", methods=["POST"])
def signup():
    email = request.json.get('email')
    username = request.json.get('username')
    password1 = request.json.get('password1')
    password2 = request.json.get('password2')

    if not username or not email:
        return jsonify({"message": "You must include a first name and email"}), 400
    
    user = User.query.filter_by(email=email).one_or_none()
    if user:
        return jsonify({"message": "Email already used!"}), 400
    
    if (password1 != password2):
        return jsonify({"message": "Passwords don't match!"}), 400
    
    new_user = User(email=email, username=username, password=generate_password_hash(
            password1, method='scrypt'))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created!"}), 201

@auth.route("/login", methods=["POST"])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    user = User.query.filter_by(email=email).one_or_none()
    if user:
            if check_password_hash(user.password, password):
                access_token = create_access_token(identity=user)
                response = make_response(jsonify({"message": "Logged in"}), 200)
                set_access_cookies(response, access_token)
                return response
            else:
                return jsonify({"message": "Wrong Email or Password!"}), 404
            
    return jsonify({"message": "Email incorrect!"}), 400

@auth.route('/logout', methods=['POST'])
def logout():
    response = jsonify({"message": "Logout successful!"})
    unset_jwt_cookies(response)
    return response

@auth.route('/get-user', methods=["GET"])
@jwt_required()
def get_user():
    favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    titlesList = []
    for favorite in favorites:
        titlesList.append(favorite.title)
    return jsonify({"user": current_user.username, "favoritesList": titlesList}), 200