from fastapi import APIRouter, Depends
from DATABASES import book_hub_users_database
from VALIDATION_FOR_USER import new_user
from sqlalchemy.orm import Session
from typing import List
from MODELS_FOR_DATABASES import model_for_users_database

'''we create an instance of the bookhub user's database to carry on querries.'''
the_users_database = model_for_users_database.USERS


'''SESSION FUNCTION FOR BOOKHUB_USERS DATABASE'''
def book_hub_users_database_session():
    the_session = book_hub_users_database.the_session_for_users()
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
    new_bookhub_user = model_for_users_database.USERS(**user_info.model_dump())
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



'''Endpoint for Logging in the user when the user has an account created.'''
@user_router.post("login", response_model =...)
def user_login(user_login_cred:...):...