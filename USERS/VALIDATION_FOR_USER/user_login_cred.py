from pydantic import BaseModel, EmailStr

'''Model validation for the user request to login.'''
class Login(BaseModel):
    user_password: str
    user_email: EmailStr


'''Model validation for the user when the request has been processed.'''
class LoginMessage(BaseModel):
    success: bool
    message: str
    Bearer: str | None = None  # JWT token
    lookup_id: str | None = None  # Kept for backward compatibility, can be removed later
    