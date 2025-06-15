from sqlalchemy.orm import declarative_base
from DATABASES import book_hub_users_database
from sqlalchemy import Column, String, INTEGER, FLOAT
    
'''We design the model of the Table we want to use for storing information
about a book.(We add the features a book has, and which we will need in the future,
for data retrieval)'''

Base = declarative_base()

class USERS(Base):
    __tablename__ =  "USERS"
    username = Column(String, index = True)
    user_id = Column(INTEGER, primary_key = True, index = True)
    email = Column(String, index = True) 
    hashed_password = Column(String, index = True)
    favourites:list =  []


'''let's create the table, using metadata'''
Base.metadata.create_all(bind = book_hub_users_database.the_engine)