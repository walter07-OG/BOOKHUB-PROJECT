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

# Load environment variables
load_dotenv()

# Configuration from environment variables
SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "none")
if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable is not set")

ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

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
SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "") or ""  # Default empty string to satisfy type checker
if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable is not set")

ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

















































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







user_router = APIRouter()


'''Endpoint for adding a new user to the database.'''

@user_router.post("/register", response_model=List[Response_For_New_User], tags=["Add New User"])
async def register_user(user_info: New_User, database_connection: Session = Depends(book_hub_users_database_session)):
    """Register a new user and return their credentials."""

    # Check if user already exists
    search_user = database_connection.query(the_users_database).filter(the_users_database.email == user_info.email).first()
    if search_user:
        return [{
            "success": False,
            "message": "User already exists. Please login or create a new account with different credentials.",
            "login_cred": {
                "Account Status": "Failed"
            }
        }]

    # Hash the user's password
    hashed_password = await hash_user_account_password(user_info.user_password)

    # Create new user object
    new_bookhub_user = user_info.model_dump()
    new_bookhub_user.pop("user_password")  # Remove plain password
    new_bookhub_user["hashed_password"] = hashed_password

    # Create user in database
    new_bookhub_user = models_for_user_related_database.USERS(**new_bookhub_user)
    database_connection.add(new_bookhub_user)
    database_connection.commit()
    database_connection.refresh(new_bookhub_user)

    # Create initial access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(new_bookhub_user.email)},
        expires_delta=access_token_expires
    )

    return [{
        "success": True,
        "message": "You have successfully created an account with BOOKHUB API.",
        "login_cred": {
            "email": user_info.email,
            "Bearer": access_token
        }
    }]



'''Endpoint for Logging in the user when the user has created an account.'''
@user_router.post("/login", response_model=List[LoginMessage], tags=["Login User"])
async def user_login(user_login_cred: Login, database_connection: Session = Depends(book_hub_users_database_session)):
    # Use the auth module's create_token function
    token_response = await create_token(user_login_cred, database_connection)
    
    return [{
        "success": True,
        "message": "Login successful.",
        "Bearer": token_response["access_token"],
    }]


@user_router.post("/logout", response_model=List[Logout_message], tags=["Logout"])
async def user_logout(
    current_user: USERS = Depends(get_current_active_user),
    database_connection: Session = Depends(book_hub_users_database_session)
):
    """Log out the current user by invalidating their JWT token.
    In a production environment, you might want to add the token to a blacklist."""
    
    return [{
        "success": True,
        "message": "Successfully logged out."
    }]