from flask import request
from flask_restx import Resource, Namespace

from app.container import genre_service
from app.dao.model.genre import GenreSchema

genre_ns = Namespace('genres')

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)

@genre_ns.route('/')
class GenreView(Resource):
    def get(self):
        genres = genre_service.get_all()
        if genres:
            return genres_schema.dump(genres), 200
        else:
            return "", 404

    def post(self):
        try:
            req_json = request.json
            genre_service.create(req_json)
            return "", 201
        except Exception:
            return "", 404

@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    def get(self, gid: int):
        try:
            genre = genre_service.get_one(gid)
            return genre_schema.dump(genre), 200
        except Exception:
            return "", 404

    def put(self, gid: int):
        try:
            req_json = request.json
            genre_service.update(gid, req_json)
            return "", 204
        except Exception:
            return "", 404

    def patch(self, gid: int):
        try:
            req_json = request.json
            genre_service.update_partial(gid, req_json)
            return "", 204
        except Exception:
            return "", 404

    def delete(self, gid: int):
        try:
            genre_service.delete(gid)
            return "", 204
        except Exception:
            return "", 404
