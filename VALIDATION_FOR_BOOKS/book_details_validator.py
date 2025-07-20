from pydantic import BaseModel
from ENDPOINT_VALIDATIONS.add_book_validator import AddBook

'''the validator for returning the book details using book ID'''

'''The validator for the response of the query'''
class Response_For_Book_Details(BaseModel):
    status: str
    message: str
    data: AddBook | None