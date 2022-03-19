# app.py

from flask import Flask, request
from flask_restx import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from schema_app import MovieSchema, GenreSchema, DirectorSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

movie_ns = api.namespace('movies')
genre_ns = api.namespace('genres')
director_ns = api.namespace('directors')


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


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
            movies = Movie.query.filter_by(director_id=director_id, genre_id=genre_id).all()
        elif director_id:
            movies = Movie.query.filter_by(director_id=director_id).all()
        elif genre_id:
            movies = Movie.query.filter_by(genre_id=genre_id).all()
        else:
            movies = Movie.query.all()
        if movies:
            return movies_schema.dump(movies), 200
        else:
            return "", 404


@movie_ns.route('/<int:mid>')
class MoviesView(Resource):
    def get(self, mid: int):
        try:
            movie = Movie.query.get(mid)
            movie_schema = MovieSchema()
            return movie_schema.dump(movie), 200
        except Exception as e:
            return "", 404


@director_ns.route('/')
class DirectorView(Resource):
    def get(self):
        directors_schema = DirectorSchema(many=True)
        directors = Director.query.all()
        if directors:
            return directors_schema.dump(directors), 200
        else:
            return "", 404

    def post(self):
        req_json = request.json
        new_director = Director(**req_json)
        with db.session.begin():
            db.session.add(new_director)
        return "", 201


@director_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did: int):
        try:
            director = Director.query.get(did)
            director_schema = DirectorSchema()
            return director_schema.dump(director), 200
        except Exception as e:
            return "", 404

    def put(self, did: int):
        director = Director.query.get(did)
        if director:
            req_json = request.json
            director.name = req_json.get("name")
            db.session.add(director)
            db.session.commit()
            return "", 204
        else:
            return "", 404

    def delete(self, did: int):
        director = Director.query.get(did)
        if director:
            db.session.delete(director)
            db.session.commit()
            return "", 204
        else:
            return "", 404


@genre_ns.route('/')
class GenreView(Resource):
    def get(self):
        genres_schema = GenreSchema(many=True)
        genres = Genre.query.all()
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
        try:
            genre = Genre.query.get(gid)
            genre_schema = GenreSchema()
            return genre_schema.dump(genre), 200
        except Exception as e:
            return "", 404

    def put(self, gid: int):
        genre = Genre.query.get(gid)
        if genre:
            req_json = request.json
            genre.name = req_json.get("name")
            db.session.add(genre)
            db.session.commit()
            return "", 204
        else:
            return "", 404

    def delete(self, gid: int):
        genre = Genre.query.get(gid)
        if genre:
            db.session.delete(genre)
            db.session.commit()
            return "", 204
        else:
            return "", 404


if __name__ == '__main__':
    app.run(debug=True)
