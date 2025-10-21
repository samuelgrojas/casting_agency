import os
from datetime import datetime, date
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
from flask_cors import CORS

from database.models import db_drop_and_create_all, setup_db, Movie, Actor, db
from auth.auth import AuthError, requires_auth
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
setup_db(app)
CORS(app)

# WARNING: db_drop_and_create_all() will clear the database.
# Controla su ejecución con la variable de entorno DROP_DB_ON_STARTUP.
if os.getenv('DROP_DB_ON_STARTUP', 'false').lower() in ('1', 'true', 'yes'):
    with app.app_context():
        db_drop_and_create_all()


# ROUTES
@app.route('/')
def index():
    return jsonify({"success": True, "message": "Casting Agency API"}), 200


@app.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors(payload):
    try:
        actors = Actor.query.order_by(Actor.id).all()
        return jsonify({
            "success": True,
            "actors": [a.format() for a in actors]
        }), 200
    except Exception as e:
        print(e)
        abort(500)


@app.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies(payload):
    try:
        movies = Movie.query.order_by(Movie.id).all()
        return jsonify({
            "success": True,
            "movies": [m.format() for m in movies]
        }, 200)
    except Exception as e:
        print(e)
        abort(500)


@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def post_actor(payload):
    try:
        body = request.get_json()
        if not body:
            abort(400)

        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')

        if name is None or age is None or gender is None:
            abort(400)

        actor = Actor(name=name, age=int(age), gender=gender)
        actor.insert()

        return jsonify({
            "success": True,
            "actor": actor.format()
        }), 200
    except (ValueError, TypeError) as e:
        print(e)
        abort(422)
    except Exception as e:
        print(e)
        abort(500)


@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def post_movie(payload):
    try:
        body = request.get_json()
        if not body:
            abort(400)

        title = body.get('title')
        release_date = body.get('release_date')  # expect 'YYYY-MM-DD'

        if title is None or release_date is None:
            abort(400)

        rd = datetime.strptime(release_date, '%Y-%m-%d').date()
        movie = Movie(title=title, release_date=rd)
        movie.insert()

        return jsonify({
            "success": True,
            "movie": movie.format()
        }), 200
    except ValueError as e:
        print(e)
        abort(422)
    except Exception as e:
        print(e)
        abort(500)


@app.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actors')
def patch_actor(payload, actor_id):
    try:
        actor = Actor.query.get(actor_id)
        if actor is None:
            abort(404)

        body = request.get_json()
        if not body:
            abort(400)

        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        if name is not None:
            actor.name = name
        if age is not None:
            actor.age = int(age)
        if gender is not None:
            actor.gender = gender

        actor.update()

        return jsonify({
            "success": True,
            "actor": actor.format()
        }), 200
    except (ValueError, TypeError) as e:
        print(e)
        abort(422)
    except Exception as e:
        print(e)
        abort(500)


@app.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movies')
def patch_movie(payload, movie_id):
    try:
        movie = Movie.query.get(movie_id)
        if movie is None:
            abort(404)

        body = request.get_json()
        if not body:
            abort(400)

        title = body.get('title', None)
        release_date = body.get('release_date', None)

        if title is not None:
            movie.title = title
        if release_date is not None:
            movie.release_date = datetime.strptime(release_date, '%Y-%m-%d').date()

        movie.update()

        return jsonify({
            "success": True,
            "movie": movie.format()
        }), 200
    except ValueError as e:
        print(e)
        abort(422)
    except Exception as e:
        print(e)
        abort(500)


@app.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(payload, actor_id):
    try:
        actor = Actor.query.get(actor_id)
        if actor is None:
            abort(404)

        actor.delete()

        return jsonify({
            "success": True,
            "delete": actor_id
        }), 200
    except Exception as e:
        print(e)
        abort(500)


@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(payload, movie_id):
    try:
        movie = Movie.query.get(movie_id)
        if movie is None:
            abort(404)

        movie.delete()

        return jsonify({
            "success": True,
            "delete": movie_id
        }), 200
    except Exception as e:
        print(e)
        abort(500)


# Error Handling
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify({
        "success": False,
        "error": ex.status_code,
        "message": ex.error.get('description', 'authorization error')
    })
    response.status_code = ex.status_code
    return response


if __name__ == '__main__':
    app.run(debug=True)
