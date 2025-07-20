from sqlalchemy.orm import declarative_base
from MODELS_FOR_DATABASES.book_database import the_engine
from sqlalchemy import Column, String, INTEGER, FLOAT, DateTime
from sqlalchemy.sql import func
    
'''We design the model of the Table we want to use for storing information
about a book.(We add the features a book has, and which we will need in the future,
for data retrieval)'''

Base = declarative_base()

class Book(Base):
    __tablename__ =  "BOOKS"
    book_id = Column(INTEGER, primary_key = True, index = True)
    book_title = Column(String, index = True)
    book_author = Column(String, index = True)
    book_genre = Column(String, index = True)
    book_description = Column(String, index = True)
    book_year = Column(INTEGER, index = True)
    book_price = Column(FLOAT, index = True)
    added_at = Column(DateTime, default=func.now())


'''let's create the table, using metadata'''
Base.metadata.create_all(bind = the_engine)