from fastapi import APIRouter, Depends, Request, status, HTTPException
from MODELS_FOR_DATABASES import book_hub_user_related_database
from .VALIDATION_FOR_USER.new_user import New_User, Response_For_New_User
from .VALIDATION_FOR_USER.user_login_cred import Login, LoginMessage
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
    #This is the code to store against the lookup_id column to use for faster query for the user's hashed api token.
    lookup_id:str = api_token[0:6]   
    #This is the actual api token to hash to the database of the user, to use for authorization.   
           
    
    return [lookup_id, api_token]


def hash_api_token(actual_secret: str) -> str:
    """Hash the generated api token to store to the database."""
    hashed_secret:str = bcrypt.hash(actual_secret)
    return hashed_secret


def verify_api_token(raw_api_token, hashed_api_token) -> bool:
    """Verify the raw api token in the request header, against the queried hashed api token."""
    verify:bool = bcrypt.verify(raw_api_token, hashed_api_token)
    
    return verify




def hash_user_account_password(user_password:str) -> str:
    """Hash a user's password before storing to the database."""
    hashed_password:str = bcrypt.hash(user_password)
    return hashed_password


def verify_user_password(raw_user_password:str, hashed_user_password:str) -> bool:
    """Verify the user's password before carrying out any operation."""
    verify:bool = bcrypt.verify(raw_user_password, hashed_user_password)
    return verify


'''we create an instance of the bookhub user's database to carry on querries.'''
the_users_database = models_for_user_related_database.USERS


'''SESSION FUNCTION FOR BOOKHUB_USERS DATABASE'''
def book_hub_users_database_session():
    the_session = book_hub_user_related_database.the_session_for_users()
    try:
        yield the_session
    finally:
        the_session.close()


def get_api_token(request: Request, database_connection: Session = Depends(book_hub_users_database_session)) -> bool:
    '''This function is used to get the API token from the user's request header.'''
    
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
        )
    raw_api_token = auth_header.split(" ", 1)[1]

    lookup_id = raw_api_token[0:6]
    user_api_token = raw_api_token[6:]
    
    '''Query the database using the lookup_id to get the hashed api_token'''
    user_row = database_connection.query(the_users_database).filter(the_users_database.lookup_id == lookup_id).first()
    if not user_row:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API token",
        )
    hashed_api_token = user_row.hashed_secret
    is_member = verify_api_token(user_api_token, hashed_api_token)
    return is_member




user_router = APIRouter()


'''Endpoint for adding a new user to the database.'''

@user_router.post("/register_user", response_model = List[Response_For_New_User], tags=["Add New User"])
def register_user(user_info: New_User, database_connection: Session = Depends(book_hub_users_database_session)):
    '''This endpoint is responsible for creating a new instance of a user.'''

    search_user = database_connection.query(the_users_database).filter(the_users_database.email == user_info.email).first()
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
    
    #this is the actual password of the user to hash in the database.
    user_password_to_hash = user_info.user_password

    #this is the generation of the api token to use by the user.
    api_token_to_use:list = generate_api_token()

    #this is the hashing of the actual api token of the user.
    hashed_secret:str = hash_api_token(api_token_to_use[1])

    #This is the hashing of the user's password.
    hashed_password:str = hash_user_account_password(user_password_to_hash)     

    #this is the lookup_id to use for fast checking of the database to verify a user's api token or membership.
    look_up_id:str = api_token_to_use[0]      




    new_bookhub_user = user_info.model_dump()

    #Remove or pop away the user_password key
    new_bookhub_user.pop("user_password")

    new_bookhub_user["lookup_id"] = look_up_id
    new_bookhub_user["hashed_secret"] = hashed_secret
    new_bookhub_user["hashed_password"] = hashed_password

    new_bookhub_user = models_for_user_related_database.USERS(**new_bookhub_user)

    database_connection.add(new_bookhub_user)
    database_connection.commit()
    database_connection.refresh(new_bookhub_user)

    return [
        {
            "success": True,
            "message": "You have successfully created an account with BOOKHUB API.",
            "login_cred": {
                "password": user_info.user_password,
                "email": user_info.email,
                "Bearer": api_token_to_use[1]
            }
        }
    ]



'''Endpoint for Logging in the user when the user has created an account.'''
@user_router.post("/login", response_model=List[LoginMessage], tags=["Login User"])
def user_login(user_login_cred: Login, database_connection: Session = Depends(book_hub_users_database_session)):
    # Find user by email
    user = database_connection.query(the_users_database).filter(the_users_database.email == user_login_cred.user_email).first()
    if not user:
        return [{
            "success": False,
            "message": "User not found. Please register first."
        }]
    

    # Ensure hashed_password is a string (should be if ORM is set up correctly)
    hashed_password = user.hashed_password if isinstance(user.hashed_password, str) else str(user.hashed_password)

    # Verify password
    if not verify_user_password(user_login_cred.user_password, hashed_password):
        return [{
            "success": False,
            "message": "Incorrect password."
        }]

    # Return the user's API token (or generate a new one if you want to rotate tokens)
    # Here, we return the existing token for simplicity
    return [{
        "success": True,
        "message": "Login successful.",
        "Bearer": user.hashed_secret,
        "lookup_id": user.lookup_id
    }]