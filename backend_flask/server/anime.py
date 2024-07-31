from flask import request, jsonify, redirect, Blueprint, make_response
from .JupyterModel import similar_animes, search, searchID
from . import jwt, db
from .models import User, Favorite
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required, current_user, unset_jwt_cookies, set_access_cookies

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()

anime = Blueprint('anime', __name__)

@anime.route('/anime/getRecs', methods=['GET'])
def get_recs():
    title = request.args.get('query')
    animeid = int(searchID(title).iloc[0]["uid"])
    return jsonify(similar_animes(animeid))

@anime.route('/anime/search', methods=['GET'])
def find():
    title = request.args.get('query')
    return jsonify(search(title))

@anime.route('/anime/add-fav', methods=['POST'])
@jwt_required()
def add_fav():
    title = request.json.get('animeTitle')
    favorites = Favorite.query.filter_by(title=title).all()
    exists = False
    for favorite in favorites:
        if favorite.user_id == current_user.id:
            exists = True
    if not exists:
        new_favorite = Favorite(title=title, user_id=current_user.id)
        db.session.add(new_favorite)
        db.session.commit()

    response = make_response(jsonify({"message": "Added Title"}), 200)
    return response

@anime.route('/anime/remove-fav', methods=['POST'])
@jwt_required()
def remove_fav():
    title = request.json.get('animeTitle')
    favorites = Favorite.query.filter_by(title=title).all()
    for favorite in favorites:
        if favorite.user_id == current_user.id:
            db.session.delete(favorite)
            db.session.commit()

    response = make_response(jsonify({"message": "Removed Title"}), 200)
    return response

@anime.route('/anime/get-fav', methods=['GET'])
@jwt_required()
def get_fav():
    favoritesList = []
    for favorite in current_user.favorites:
        favoritesList.append(search(favorite.title)[0])

    return jsonify(favoritesList)