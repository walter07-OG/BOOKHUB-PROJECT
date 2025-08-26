from pydantic import BaseModel
from BOOKS.VALIDATION_FOR_BOOKS.add_book_validator import AddBook

class BookSearchResponse(BaseModel):
    message: str
    book_info: AddBook
    success: bool