import datetime
from app import app
from models import db, Reservation, User,Author,Book

with app.app_context():
    
    # Delete all rows in tables
    
    Reservation.query.delete()
    User.query.delete()
    Author.query.delete()
    Book.query.delete()
    # users
  
    # Add projects



 

    a1 = Author(name="Ben Curson")
    a2 =Author (name="Unknown")
    a3 = Author( name="jane kariuki")
    db.session.add_all([a1,a2,a3])
    db.session.commit()
     
    b1 = Book(title="Gifted hand", image= "https://textbookcentre.com/media/products/2030307000001_1.jpg", author=a1)
    b2 = Book(title="All the men in lagos are mad", image= "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTj3BQ3DrmatnneqDMLXR4hWr1DAwv2j8OWjuqRUZMY4Q&s", author=a2)
    b3 = Book(title="Confessions of nirobi women", image= "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS_ZEuhaza0Yu1Of9oUA9MATR1-7lqH2s2KE3VSf4172A&s",  author=a3)

    db.session.add_all([b1,b2,b3])
    db.session.commit()

      
    r1 = Reservation(reservation_date=datetime.datetime(2023, 5, 28),book=b1)
    r2 = Reservation(reservation_date=datetime.datetime(2022, 6, 2),book=b2)
    r3 = Reservation(reservation_date=datetime.datetime(2023, 7, 8),book=b3)
    

    db.session.add_all([r1,r2,r3])
    db.session.commit()

    pass