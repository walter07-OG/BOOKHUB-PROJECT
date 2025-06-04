from sqlalchemy.orm import declarative_base
from DATABASES import favourite_book_database
from sqlalchemy import Column, String
from typing import List
    
'''We design the model of the Table we want to use for storing information
about a book.(We add the features a book has, and which we will need in the future,
for data retrieval)'''

Base = declarative_base()

class Book(Base):
    __tablename__ =  "USER_FAVOURITES"
    '''NOTE: If two hashed passwords cannot be the same,  then we will use the hashed passwords 
    as the primary key.'''
    user_password = Column(String, primary_key = True, index = True)
    user_favourites = Column(, index = True)

'''let's create the table, using metadata'''
Base.metadata.create_all(bind = favourite_book_database.the_engine)