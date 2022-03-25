from flask import request
from flask_restx import Resource, Namespace, reqparse

from app.container import movie_service
from app.dao.model.movie import MovieSchema

movie_ns = Namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        pass
        parser = reqparse.RequestParser()
        parser.add_argument('director_id')
        parser.add_argument('genre_id')
        parser.add_argument('year')
        params = parser.parse_args()

        movies_schema = MovieSchema(many=True)
        director_id = params['director_id']
        genre_id = params['genre_id']
        year = params['year']

        # director_id = request.args.get('director_id')
        # genre_id = request.args.get('genre_id')

        filters = {
            "director_id": director_id,
            "genre_id": genre_id,
            "year": year,

        }

        movies = movie_service.get_by_param(filters)
        if movies:
            return movies_schema.dump(movies), 200
        else:
            return "", 404

    def post(self):
        try:
            req_json = request.json
            movie_service.create(req_json)
            return "", 201
        except Exception:
            return "", 404


@movie_ns.route('/<int:mid>')
class MoviesView(Resource):
    def get(self, mid: int):
        try:
            movie = movie_service.get_one(mid)
            return movie_schema.dump(movie), 200
        except Exception:
            return "", 404


    def put(self, mid: int):
        try:
            req_json = request.json
            if "id" not in req_json:
                req_json["id"] = mid
            movie_service.update(req_json)
            return "", 204
        except Exception:
            return "", 404


    def patch(self, mid: int):
        try:
            req_json = request.json
            if "id" not in req_json:
                req_json["id"] = mid
            movie_service.update_partial(mid, req_json)
            return "", 204
        except Exception:
            return "", 404

    def delete(self, mid: int):
        try:
            movie_service.delete(mid)
            return "", 204
        except Exception:
            return "", 404