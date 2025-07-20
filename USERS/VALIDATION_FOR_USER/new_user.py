from pydantic import BaseModel, EmailStr
from typing import Dict


'''Model validation for the user, when the user sends a request.'''
class New_User(BaseModel):
    username: str
    email: EmailStr
    user_password: str
    



'''Model validation for the response to the user, when the user adds an account'''
class Response_For_New_User(BaseModel):
    success: bool
    message: str
    login_cred: Dict[str, str]