from flask import request
from flask_restx import Resource, Namespace

from app.database import db
from app.models import Genre
from app.schema_app import GenreSchema

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenreView(Resource):
    def get(self):
        genres = db.session.query(Genre).all()
        genres_schema = GenreSchema(many=True)
        if genres:
            return genres_schema.dump(genres), 200
        else:
            return "", 404

    def post(self):
        req_json = request.json
        new_genre = Genre(**req_json)
        with db.session.begin():
            db.session.add(new_genre)
        return "", 201


@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    def get(self, gid: int):
        genre = db.session.query(Genre).get(gid)
        genre_schema = GenreSchema()
        if genre:
            return genre_schema.dump(genre), 200
        else:
            return "", 404
        # try:
        #     genre = Genre.query.get(gid)
        #     genre_schema = GenreSchema()
        #     return genre_schema.dump(genre), 200
        # except Exception as e:
        #     return "", 404

    def put(self, gid: int):
        genre = db.session.query(Genre).get(gid)
        if genre:
            req_json = request.json
            genre.name = req_json.get("name")
            db.session.add(genre)
            db.session.commit()
            return "", 204
        else:
            return "", 404

    def delete(self, gid: int):
        genre = db.session.query(Genre).get(gid)
        if genre:
            db.session.delete(genre)
            db.session.commit()
            return "", 204
        else:
            return "", 404
