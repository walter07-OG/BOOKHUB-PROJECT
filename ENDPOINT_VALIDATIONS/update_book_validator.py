from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

current_year = datetime.now().year

'''This class is used to validate an incoming request from the user, trying to update an/the attributes of a book.'''
class UpdateBookId(BaseModel):
    book_id: int = Field(gt = 0) 
    book_title: Optional[str]
    book_author: Optional[str]
    book_genre: Optional[str]
    book_year: int = Field(ge=1000, le=current_year)
    book_price: float = Field(gt = 0)
    book_description: Optional[str]



'''This class is used to validate the output sent to the user after an update was made to
books/book in the database.'''
class UpdateBookIdResponse(BaseModel):
    message: str
    success: bool
    code: int
    new_price: float