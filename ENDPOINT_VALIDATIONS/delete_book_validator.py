from pydantic import BaseModel
from typing import Dict

'''This validator model or class is to validate the incoming json from the user to delete a book from the database.'''
class DeleteBook(BaseModel):
    book_id: int


'''This is the validation for validating the output after a book has been successfully deleted.'''
class DeleteBookResponse(BaseModel):
    message: str
    book_deleted_info: Dict[str, str | int | float]
    success: bool