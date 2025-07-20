from sqlalchemy.orm import declarative_base, relationship
from MODELS_FOR_DATABASES.book_hub_user_related_database import the_engine
from sqlalchemy import Column, String, ForeignKey, JSON, DateTime, Integer, Boolean
from sqlalchemy.sql import func


Base = declarative_base()

class USERS(Base):
    __tablename__ =  "USERS"
    member_id = Column(Integer, primary_key=True, autoincrement=True)
    lookup_id = Column(String, index=True, unique=True, nullable=False)
    hashed_secret = Column(String, unique=True, nullable=False)
    user_id_available = Column(Boolean, index=True, default=False)
    hashed_password = Column(String, index=True, nullable=False, unique=True)
    username = Column(String, index=True)
    email = Column(String, index=True, unique=True, nullable=False)
    apikey_updated  = Column(String, index=True, default=func.now(), onupdate=func.now())
    apikey_expires = Column(String, index=True, default=func.now())
    favourites = relationship("FAVOURITE_BOOKS", back_populates="user")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    


'''class for the favourites database.'''
class FAVOURITE_BOOKS(Base):
    __tablename__ =  "USER_FAVOURITES"
    favourites_id = Column(Integer, index=True)
    hashed_secret = Column(String, ForeignKey("USERS.hashed_secret"), primary_key=True, index=True)
    user_favourites = Column(JSON, index=True, default=[])
    user = relationship("USERS", back_populates="favourites")


'''let's create the table, using metadata'''
Base.metadata.create_all(bind = the_engine)