from flask_restx import Resource, Namespace, reqparse

from app.database import db
from app.models import Movie
from app.schema_app import MovieSchema

movie_ns = Namespace('movies')


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('director_id')
        parser.add_argument('genre_id')
        params = parser.parse_args()

        movies_schema = MovieSchema(many=True)
        director_id = params['director_id']
        genre_id = params['genre_id']
        # director_id = request.args.get('director_id')
        # genre_id = request.args.get('genre_id')
        if director_id and genre_id:
            movies = db.session.query(Movie).filter(director_id=director_id, genre_id=genre_id).all()
        elif director_id:
            movies = db.session.query(Movie).filter(director_id=director_id).all()
        elif genre_id:
            movies = db.session.query(Movie).filter(genre_id=genre_id).all()
        else:
            movies = db.session.query(Movie).all()
        if movies:
            return movies_schema.dump(movies), 200
        else:
            return "", 404


@movie_ns.route('/<int:mid>')
class MoviesView(Resource):
    def get(self, mid: int):
        movie = db.session.query(Movie).get(mid)
        movie_schema = MovieSchema()
        if movie:
            return movie_schema.dump(movie), 200
        else:
            return "", 404
