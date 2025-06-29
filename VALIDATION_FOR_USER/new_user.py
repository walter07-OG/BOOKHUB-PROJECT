from pydantic import BaseModel

'''Model validation for the user, when the user sends a request.'''
class New_User(BaseModel):
    user_name: str
    user_email: str
    user_password: int
    user_favourites: list 


'''Model validation for the response to the user, when the user adds an account'''
class Response_For_New_User(BaseModel):
    success: bool
    message: str
    login_id: int