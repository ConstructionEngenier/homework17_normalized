from flask import request
from flask_restx import Resource, Namespace

from app.container import director_service
from app.dao.model.director import DirectorSchema

director_ns = Namespace('directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

@director_ns.route('/')
class DirectorView(Resource):
    def get(self):
        directors = director_service.get_all()
        if directors:
            return directors_schema.dump(directors), 200
        else:
            return "", 404

    def post(self):
        try:
            req_json = request.json
            director_service.create(req_json)
            return "", 201
        except Exception:
            return "", 404

@director_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did: int):
        try:
            director = director_service.get_one(did)
            return director_schema.dump(director), 200
        except Exception:
            return "", 404

    def put(self, did: int):
        try:
            req_json = request.json
            director_service.update(did, req_json)
            return "", 204
        except Exception:
            return "", 404


    def patch(self, did: int):
        try:
            req_json = request.json
            director_service.update_partial(did, req_json)
            return "", 204
        except Exception:
            return "", 404

    def delete(self, did: int):
        try:
            director_service.delete(did)
            return "", 204
        except Exception:
            return "", 404
