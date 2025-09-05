from sqlalchemy.orm import declarative_base, relationship
from MODELS_FOR_DATABASES.book_hub_user_related_database import the_engine
from sqlalchemy import Column, String, ForeignKey, JSON, DateTime, Integer, Boolean
from sqlalchemy.sql import func


Base = declarative_base()

class USERS(Base):
    __tablename__ =  "USERS"
    member_id = Column(Integer, primary_key=True, autoincrement=True)
    hashed_password = Column(String, index=True, nullable=False)
    username = Column(String, index=True)
    email = Column(String, index=True, unique=True, nullable=False)
    favourites = relationship("FAVOURITE_BOOKS", back_populates="user")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    


'''class for the favourites database.'''
class FAVOURITE_BOOKS(Base):
    __tablename__ =  "USER_FAVOURITES"
    favourites_id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey("USERS.member_id"), index=True, nullable=False)
    user_favourites = Column(JSON, index=True, default=[])
    user = relationship("USERS", back_populates="favourites")


'''let's create the table, using metadata'''
Base.metadata.create_all(bind = the_engine)