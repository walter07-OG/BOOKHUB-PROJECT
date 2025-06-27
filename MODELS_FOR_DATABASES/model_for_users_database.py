from sqlalchemy.orm import declarative_base, relationship
from DATABASES import book_hub_users_database
from sqlalchemy import Column, String, ForeignKey
from model_for_book_database import Book
    
'''We design the model of the Table we want to use for storing information
about a book.(We add the features a book has, and which we will need in the future,
for data retrieval)'''

Base = declarative_base()

class USERS(Base):
    __tablename__ =  "USERS"
    hashed_password = Column(String, ForeignKey("USER_FAVOURITES.user_password"), primary_key = True)
    username = Column(String, index = True)
    email = Column(String, index = True) 
    user_favourites = relationship("FAVOURITE_BOOKS", back_populates = "user_favourites")

'''let's create the table, using metadata'''
Base.metadata.create_all(bind = book_hub_users_database.the_engine)