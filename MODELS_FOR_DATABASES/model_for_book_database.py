from sqlalchemy.orm import declarative_base
from DATABASES import book_database
from sqlalchemy import Column, String, INTEGER, FLOAT
    
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

'''let's create the table, using metadata'''
Base.metadata.create_all(bind = book_database.the_engine)