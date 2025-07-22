from pydantic import BaseModel

class Logout(BaseModel):
    '''The validation class for logging out the user.(request)'''
    #We initiate the get_api_token() function to extract the user's Bearer token to add it to
    #the blacklist, preventing the user from making an additional request after logging out.



class Logout_message(BaseModel):
    '''The validation for the success message after the user successfully logs out.'''
    success: bool
    message: str