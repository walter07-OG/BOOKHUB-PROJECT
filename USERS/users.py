from fastapi import APIRouter, Depends
from MODELS_FOR_DATABASES import book_hub_user_related_database
from VALIDATION_FOR_USER import new_user, user_login_cred
from sqlalchemy.orm import Session
from typing import List
from MODELS_FOR_DATABASES import models_for_user_related_database
from passlib.hash import bcrypt
import secrets
import string


def generate_api_token(length=64) -> list[str]:
    """Generate a securely random API token."""
    alphabet:str = string.ascii_letters + string.digits
    api_token:str = ''.join(secrets.choice(alphabet) for i in range(length))
    lookup_id:str = api_token[0:6]      #This is the code to store to against the lookup_id column to use for faster query for the user's hashed api token.
    actual_secret:str = api_token[7:]       #This is the actual api token to hash to the database of the user, to use for authorization.
    
    return [lookup_id, actual_secret]


def hash_api_token(actual_secret: str) -> str:
    """Hash the generated api token to store to the database."""
    hashed_secret:str = bcrypt.hash(actual_secret)
    return hashed_secret


def verify_api_token(raw_api_token, hashed_api_token):
    """Verify the raw api token in the request header, against the queried hashed api token."""
    verify = bcrypt.verify(raw_api_token, hashed_api_token)



'''we create an instance of the bookhub user's database to carry on querries.'''
the_users_database = models_for_user_related_database.USERS


'''SESSION FUNCTION FOR BOOKHUB_USERS DATABASE'''
def book_hub_users_database_session():
    the_session = book_hub_user_related_database.the_session_for_users()
    try:
        yield the_session
    finally:
        the_session.close()


user_router = APIRouter()


'''Endpoint for adding a new user to the database.'''

@user_router.post("/register_user", response_model = List[new_user.Response_For_New_User])
def register_user(user_info: new_user.New_User, database_connection: Session = Depends(book_hub_users_database_session)):
    '''This endpoint is responsible for creating a new instance of a user.'''
    search_user = database_connection.query(the_users_database).filter(the_users_database.hashed_password == user_info.user_password)
    if search_user:
        '''Return message when the user already exists.'''
        return [
            {
                "success": False,
                "message": "Sorry, the user with the entered credentials already exists. Try logging in using the login"
                "endpoint rather. Or better still, create a new account.",
                "login_cred": {
                    "Account Status": "Failed."
                }
            }
        ]
    
    '''Operations and return message when the user is new to the database.'''
    new_bookhub_user = models_for_user_related_database.USERS(**user_info.model_dump())
    database_connection.add(new_bookhub_user)
    database_connection.commit()
    database_connection.refresh(new_bookhub_user)

    return [
        {
            "success": True,
            "message": "You have successfully created an account with BOOKHUB API.",
            "login_cred": {
                "password": user_info.user_password,
                "email": user_info.user_email
            }
        }
    ]



'''Endpoint for Logging in the user when the user has created an account.'''
@user_router.post("login", response_model = List[user_login_cred.LoginMessage])
def user_login(user_login_cred: user_login_cred.Login, database_connection: Session = Depends(book_hub_users_database_session)):...