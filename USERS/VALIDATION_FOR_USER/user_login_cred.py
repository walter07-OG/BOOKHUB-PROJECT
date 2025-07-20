from pydantic import BaseModel

'''Model validation for the user request to login.'''
class Login(BaseModel):
    user_password: str
    user_email: str


'''Model validation for the user when the request has been processed.'''
class LoginMessage(BaseModel):
    success: bool
    message: str
    