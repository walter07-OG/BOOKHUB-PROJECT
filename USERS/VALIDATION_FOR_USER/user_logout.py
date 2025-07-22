from pydantic import BaseModel

class Logout_message(BaseModel):
    '''The validation for the success message after the user successfully logs out.'''
    success: bool
    message: str