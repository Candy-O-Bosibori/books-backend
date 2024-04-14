# import flask
from flask import Flask,jsonify,request, make_response
from flask_restful import Api, Resource

from models import User,Book,Author, Reservation
from extentions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, create_refresh_token, jwt_required


from flask_restx import Api, Resource, fields, Namespace

auth_ns = Namespace('auth', description='A name space for our authentication ')


# SIGNUP
class Signup(Resource):
    def post(self):
        # get data from front end
        data = request.get_json()

        # check if the user exists
        username = data['username']
        db_user= User.query.filter(User.username==username).first()

        # return error if they exist
        if db_user is not  None:
            return jsonify({"massege'":f"uaer name already exists"})
        
        # create a new user
        new_user = User(
            username = data['username'],
            email = data['email'],
            # pass posted password into the Generate_password_hash has to be hashed 
            password =generate_password_hash(data['password'])

        
        )
        new_user.save()
        
        return make_response(new_user.to_dict(), 201)



auth_ns.add_resource(Signup, '/signup')


# LOGIN
class Login(Resource):
    def post(self):
        username = request.get_json()['username']
        password = request.get_json()['password']

        db_user= User.query.filter(User.username==username).first()

        if db_user and check_password_hash(db_user.password, password):
            access_token = create_access_token(identity=db_user.username)
            refresh_token = create_refresh_token(identity=db_user.username)
            
            return jsonify({"access_token":access_token, "refresh":refresh_token})

         
        pass

        
auth_ns.add_resource(Login, '/login')

@auth_ns.route("/refresh")
class RefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):

        current_user = get_jwt_identity()

        new_access_token = create_access_token(identity=current_user)

        return make_response(jsonify({"access_token": new_access_token}), 200)