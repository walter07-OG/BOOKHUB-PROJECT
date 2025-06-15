from pydantic import BaseModel
from ENDPOINT_VALIDATIONS.add_book_validator import AddBook


'''This class is used to validate an incoming request from the user, trying to update an/the attributes of a book.'''
class UpdateBookId(BaseModel):
    book_id: int
    book_updates: AddBook


'''This class is used to validate the output sent to the user after an update was made to
books/book in the database.'''
class UpdateBookIdResponse(BaseModel):
    message: str
    success: bool
    code: int