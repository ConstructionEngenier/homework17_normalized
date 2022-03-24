from flask import request
from flask_restx import Resource, Namespace

from app.database import db
from app.models import Director
from app.schema_app import DirectorSchema

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorView(Resource):
    def get(self):
        directors = db.session.query(Director).all()
        directors_schema = DirectorSchema(many=True)
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
        director = db.session.query(Director).get(did)
        director_schema = DirectorSchema()
        if director:
            return director_schema.dump(director), 200
        else:
            return "", 404
        # try:
        #     director = Director.query.get(did)
        #     director_schema = DirectorSchema()
        #     return director_schema.dump(director), 200
        # except Exception as e:
        #     return "", 404

    def put(self, did: int):
        director = db.session.query(Director).get(did)
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
