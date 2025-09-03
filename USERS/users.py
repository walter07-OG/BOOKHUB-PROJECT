#Codes for the user's endpoints
from fastapi import APIRouter, Depends, Request, status, HTTPException
from MODELS_FOR_DATABASES import book_hub_user_related_database
from .VALIDATION_FOR_USER.new_user import New_User, Response_For_New_User
from .VALIDATION_FOR_USER.user_login_cred import Login, LoginMessage
from .VALIDATION_FOR_USER.user_logout import Logout_message
from sqlalchemy.orm import Session
from typing import List
from MODELS_FOR_DATABASES import models_for_user_related_database
from passlib.hash import bcrypt
import secrets
import string




















#The codes imported from the auth file.
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from MODELS_FOR_DATABASES.models_for_user_related_database import USERS
from MODELS_FOR_DATABASES.book_hub_user_related_database import the_session_for_users
from .VALIDATION_FOR_USER.user_login_cred import Login

# Configuration
# WARNING: In production, these values should be loaded from environment variables
# using python-dotenv or similar secure configuration management

SECRET_KEY = "your-secret-key-keep-it-safe"  # CRITICAL: Must be changed in production
ALGORITHM = "HS256"  # Industry standard for JWT signing
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token validity duration


# OAuth2 scheme for Swagger UI and authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password using bcrypt."""
    return await verify_user_password(plain_password, hashed_password)

def get_user(db: Session, email: str) -> Optional[USERS]:
    """Retrieve user from database by email."""
    return db.query(USERS).filter(USERS.email == email).first()


async def authenticate_user(db: Session, email: str, password: str) -> Optional[USERS]:
    """Authenticate user credentials."""
    user = get_user(db, email)
    if not user:
        return None
    
    # Ensure hashed_password is a string
    hashed_password = user.hashed_password if isinstance(user.hashed_password, str) else str(user.hashed_password)
    
    if not await verify_password(password, hashed_password):
        return None
    return user


def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(the_session_for_users)
) -> USERS:
    """Get current user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = get_user(db, str(email))
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: USERS = Depends(get_current_user)) -> USERS:
    """Get current active user."""
    return current_user

# Token endpoint
async def create_token(form_data: Login, db: Session) -> Dict:
    """Create access token for valid credentials."""
    user = await authenticate_user(db, form_data.user_email, form_data.user_password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.email)},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# Load environment variables
load_dotenv()

# Configuration from environment variables
SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "")
if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable is not set")

ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

#the codes












































async def generate_api_token(length=64) -> list[str]:
    """Generate a securely random API token."""
    alphabet:str = string.ascii_letters + string.digits
    api_token:str = ''.join(secrets.choice(alphabet) for i in range(length))
    #This is the code to store against the lookup_id column to use for faster query for the user's hashed api token.
    lookup_id:str = api_token[0:6]   
    #This is the actual api token to hash to the database of the user, to use for authorization.   
           
    
    return [lookup_id, api_token]


async def hash_api_token(actual_secret: str) -> str:
    """Hash the generated api token to store to the database."""
    hashed_secret:str = bcrypt.hash(actual_secret)
    return hashed_secret


async def verify_api_token(raw_api_token, hashed_api_token) -> bool:
    """Verify the raw api token in the request header, against the queried hashed api token."""
    verify:bool = bcrypt.verify(raw_api_token, hashed_api_token)
    
    return verify




async def hash_user_account_password(user_password:str) -> str:
    """Hash a user's password before storing to the database."""
    hashed_password:str = bcrypt.hash(user_password)
    return hashed_password


async def verify_user_password(raw_user_password:str, hashed_user_password:str) -> bool:
    """Verify the user's password before carrying out any operation."""
    verify:bool = bcrypt.verify(raw_user_password, hashed_user_password)
    return verify


'''we create an instance of the bookhub user's database to carry on querries.'''
the_users_database = models_for_user_related_database.USERS


'''SESSION FUNCTION FOR BOOKHUB_USERS DATABASE'''
async def book_hub_users_database_session():
    the_session = book_hub_user_related_database.the_session_for_users()
    try:
        yield the_session
    finally:
        the_session.close()


async def get_api_token(request: Request, database_connection: Session = Depends(book_hub_users_database_session)) -> bool:
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
    is_member = await verify_api_token(user_api_token, hashed_api_token)
    return is_member




user_router = APIRouter()


'''Endpoint for adding a new user to the database.'''

@user_router.post("/register", response_model = List[Response_For_New_User], tags=["Add New User"])
async def register_user(user_info: New_User, database_connection: Session = Depends(book_hub_users_database_session)):
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
    api_token_to_use:list = await generate_api_token()

    #this is the hashing of the actual api token of the user.
    hashed_secret:str = await hash_api_token(api_token_to_use[1])

    #This is the hashing of the user's password.
    hashed_password:str = await hash_user_account_password(user_password_to_hash)     

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
async def user_login(user_login_cred: Login, database_connection: Session = Depends(book_hub_users_database_session)):
    # Use the auth module's create_token function
    token_response = await create_token(user_login_cred, database_connection)
    
    return [{
        "success": True,
        "message": "Login successful.",
        "Bearer": token_response["access_token"],
        "lookup_id": None  # No longer needed with JWT
    }]


@user_router.post("/logout", response_model=List[Logout_message], tags=["Logout"])
async def user_logout(database_connection: Session = Depends(book_hub_users_database_session)):...
"""The logic is implemented to get the user's api token to add to the blacklist"""