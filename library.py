# import flask
from flask import Flask,jsonify,request, make_response
from models import User,Book,Author, Reservation
from extentions import db
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required


from flask_restx import Api, Resource, fields, Namespace

library_ns = Namespace('library', description='A name space for all my other routes')

#class books GET, POST
class MyBooks(Resource):
    def get(self):
        books = [book.to_dict(rules=('-reservations','-author',)) for book in Book.query.all()]
        return make_response(books, 200)

    @jwt_required()
    def post(self):
        data = request.get_json()
        new_book = Book(
            title=data['title'],
            image=data['image']

        )
        db.session.add(new_book)
        db.session.commit() 
        return make_response(new_book.to_dict(), 201)
library_ns.add_resource(MyBooks, '/books')


#class booksbyid GET, PATCH,DELETE
class MyBooksById(Resource):
    def get(self, id):
        book = Book.query.filter(Book.id == id).first()

        if book is None:
            return make_response({'error': 'Event not found'}, 404)

        return make_response(book.to_dict(rules=('-reservations.user','-reservations.book', '-author.books',)), 200)

    @jwt_required()
    def patch(self, id):
        data = request.get_json()

        book = Book.query.filter_by(id=id).first()

        for attr in data:
            setattr(book, attr, data[attr])

        db.session.add(book)
        db.session.commit()

        return make_response(book.to_dict(rules=('-reservations.user','-reservations.book', '-author.books',)), 200)

    @jwt_required()
    def delete(self, id):
        book= Book.query.filter_by(id=id).first()
        db.session.delete(book)
        db.session.commit()

        return make_response('', 204)

library_ns.add_resource(MyBooksById, '/books/<int:id>')