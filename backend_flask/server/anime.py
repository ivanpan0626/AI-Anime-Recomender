from flask import request, jsonify, redirect, Blueprint, make_response
from .JupyterModel import similar_animes, search, searchID

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
