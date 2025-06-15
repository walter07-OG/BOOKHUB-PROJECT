'''We are going to import the create engine from sqlachemy to create an engine to run
the sql database we will create and connect to sqlachemy'''
from sqlalchemy import create_engine

'''We again import the session to create a sqlalchemy session to the database  to carry out
database functions, when needed.'''
from sqlalchemy.orm import sessionmaker

'''we then define the database URL which we are going to use for our book database.
NOTE: In this case, it is SQLITE. This means it can be any of a database type.'''
database_url = "sqlite:///./USERS.db"

'''We lean into the creation of the engine of the database.'''
the_engine = create_engine(database_url, echo = True)

'''We then proceed to the building of the session factory to facillitate the creation of 
a session to perform database functions.'''
'''Settting the autocommit to be False prevents the database from 
automatically commiting.'''
'''The "bind" is responsible for linking the engine, which contains the URL for the database.'''
the_session_for_users = sessionmaker(autoflush = False, bind = the_engine)