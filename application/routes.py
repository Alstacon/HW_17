from flask import current_app as app, request
from flask_restx import Api, Namespace, Resource

from application.models import db
from application import models, schema

api: Api = app.config['api']
movie_ns: Namespace = api.namespace('movies')
director_ns: Namespace = api.namespace('directors')
genre_ns: Namespace = api.namespace('genres')

movie_schema = schema.MovieSchema()
movies_schema = schema.MovieSchema(many=True)

director_schema = schema.DirectorSchema()
directors_schema = schema.DirectorSchema(many=True)

genre_schema = schema.GenreSchema()
genres_schema = schema.GenreSchema(many=True)


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        movies_query = db.session.query(models.Movie)

        args = request.args

        director_id = args.get('director_id')
        if director_id is not None:
            movies_query = movies_query.filter(models.Movie.director_id == director_id)

        genre_id = args.get('genre_id')
        if genre_id is not None:
            movies_query = movies_query.filter(models.Movie.genre_id == genre_id)

        movies = movies_query.all()

        return movies_schema.dump(movies), 200

    def post(self):
        movie = movie_schema.load(request.json)
        db.session.add(models.Movie(**movie))
        db.session.commit()

        return None, 201


@movie_ns.route('/<int:id>')
class MovieView(Resource):
    def get(self, id):
        movie = db.session.query(models.Movie).get(id)
        if movie is None:
            return None, 404

        return movie_schema.dump(movie), 200

    def put(self, id):
        db.session.query(models.Movie).filter(models.Movie.id == id).update(request.json)
        db.session.commit()

        return None, 204

    def delete(self, id):
        delete_rows = db.session.query(models.Movie).filter(models.Movie.id == id).delete()
        if delete_rows != 1:
            return None, 404
        db.session.commit()
        return None, 204


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        directors = db.session.query(models.Director).all()

        return directors_schema.dump(directors), 200

    def post(self):
        director = director_schema.load(request.json)

        db.session.add(models.Director(**director))
        db.session.commit()

        return None, 201


@director_ns.route('/<int:id>')
class DirectorView(Resource):
    def get(self, id):
        director = db.session.query(models.Director).get(id)
        if director is None:
            return None, 404

        return director_schema.dump(director), 200

    def put(self, id):
        db.session.query(models.Director).filter(models.Director.id == id).update(request.json)
        db.session.commit()

        return None, 204

    def delete(self, id):
        delete_rows = db.session.query(models.Director).filter(models.Director.id == id).delete()
        if delete_rows != 1:
            return None, 404

        db.session.commit()
        return None, 204


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        genres = db.session.query(models.Genre).all()

        return genres_schema.dump(genres), 200

    def post(self):
        genre = genre_schema.load(request.json)

        db.session.add(models.Genre(**genre))
        db.session.commit()

        return None, 201


@genre_ns.route('/<int:id>')
class GenreView(Resource):
    def get(self, id):
        genre = db.session.query(models.Genre).get(id)
        if genre is None:
            return None, 404
        return genre_schema.dump(genre), 200

    def put(self, id):
        db.session.query(models.Genre).filter(models.Genre.id == id).update(request.json)
        db.session.commit()

        return None, 204

    def delete(self, id):
        delete_rows = db.session.query(models.Genre).filter(models.Genre.id == id).delete()
        if delete_rows != 1:
            return None, 404

        db.session.commit()
        return None, 204
