from extentions import db

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

class User(db.Model, SerializerMixin):
    __tablename__='users'
    

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable=False, unique=True)
    reservations = db.relationship('Reservation', back_populates='user',  cascade='all, delete-orphan')
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.Text(), nullable=False)

    books = association_proxy('reservations', 'book',
                                 creator=lambda book: Reservation(book=book))
    serialize_rules = ('-reservations.user',)

    def __repr__(self):
        """
        returns string rep of object

        """
        return f"<User {self.username}>"

    def save(self):
        db.session.add(self)
        db.session.commit()


class Book(db.Model, SerializerMixin):
    __tablename__='books'
    

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    reservations = db.relationship('Reservation', back_populates='book',  cascade='all, delete-orphan')
    serialize_rules = ('-reservations.book',)
    users = association_proxy('reservations', 'user', creator=lambda user: Reservation(user=user))
    author = db.relationship('Author', backref='books')

    def save(self):
       
        db.session.add(self)
        db.session.commit()

    def delete(self):
       
        db.session.delete(self)
        db.session.commit()

    def update(self, title, image, description):
      
        self.title = title
        self.description = description
        self.image = image

        db.session.commit()

class Author(db.Model, SerializerMixin):
    __tablename__='author'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def save(self):
       
        db.session.add(self)
        db.session.commit()

    def delete(self):
       
        db.session.delete(self)
        db.session.commit()

    def update(self, name):
      
        self.name=name

        db.session.commit()


class Reservation(db.Model,SerializerMixin):
    __tablename__='reservations'

    
    id = db.Column(db.Integer, primary_key=True)
    reservation_date = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))

    user= db.relationship('User', back_populates= 'reservations')
    book = db.relationship('Book', back_populates= 'reservations')
    serialize_rules = ('-users.reservations', '-events.reservations',)

    def save(self):
       
        db.session.add(self)
        db.session.commit()

    def delete(self):
       
        db.session.delete(self)
        db.session.commit()

    def update(self, reservation_date):
      
        self.reservation_date=reservation_date

        db.session.commit()
    
