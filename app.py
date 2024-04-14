# import flask
from flask import Flask
from flask_restful import Api
from flask_restx import Api
from flask_migrate import Migrate
from models import User,Book,Author, Reservation
from extentions import db
from flask_jwt_extended import JWTManager
from library import library_ns
from auth import auth_ns
from flask_cors import CORS

def create_app(config):
    app=Flask(__name__)
    app.config.from_object(config)
    CORS(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    db.init_app(app)
    api=Api(app,doc='/docs' )
    api.add_namespace(library_ns)
    api.add_namespace(auth_ns)



    @app.shell_context_processor
    def make_shell_context():
        return{
            "db":db,
            "user":User,
            "Book":Book,
            "Author":Author,
            "Reservation":Reservation

        }
    

    
    return app


    