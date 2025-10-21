import os
import json
from datetime import date
from sqlalchemy import Column, String, Integer, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

database_filename = "database/database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()

def setup_db(app):
    # si la app ya tiene SQLALCHEMY_DATABASE_URI (p. ej. desde config.Config), no lo sobreescribimos
    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    # aseguramos TRACK_MODIFICATIONS si no está definida
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    db.app = app
    db.init_app(app)

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

    # seed demo data
    m = Movie(title='The Matrix', release_date=date(1999, 3, 31))
    a = Actor(name='Keanu Reeves', age=56, gender='Male')
    m.insert()
    a.insert()

    # associate actor with movie
    m.actors.append(a)
    db.session.commit()

# association table for many-to-many Movie <-> Actor
movie_actor = Table(
    'movie_actor',
    db.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True),
    Column('actor_id', Integer, ForeignKey('actors.id'), primary_key=True)
)

class Movie(db.Model):
    __tablename__ = 'movies'
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    title = Column(String(120), nullable=False)
    release_date = Column(Date, nullable=False)

    # many-to-many relationship
    actors = relationship('Actor', secondary=movie_actor, back_populates='movies')

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.isoformat() if self.release_date else None,
            'actors': [{'id': a.id, 'name': a.name} for a in self.actors]
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.format())

class Actor(db.Model):
    __tablename__ = 'actors'
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    name = Column(String(120), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(50), nullable=False)

    # many-to-many relationship
    movies = relationship('Movie', secondary=movie_actor, back_populates='actors')

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movies': [{'id': m.id, 'title': m.title} for m in self.movies]
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.format())