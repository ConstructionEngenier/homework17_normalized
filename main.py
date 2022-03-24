# main.py

from flask import Flask
from flask_restx import Api

from app.config import Config
from app.database import db
from app.views.movies import movie_ns
from app.views.directors import director_ns
from app.views.genres import genre_ns


def create_app(config: Config) -> Flask:
    application = Flask(__name__)
    application.config.from_object(config)
    application.app_context().push()
    return application


def configure_app(application: Flask):
    db.init_app(application)
    api = Api(app)
    api.add_namespace(movie_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(director_ns)


app_config = Config()
app = create_app(app_config)
configure_app(app)
app.debug = True


if __name__ == '__main__':
    app.run()
