from pydantic import BaseModel
from .add_book_validator import AddBook
from typing import List

'''The validation class for get_all_books() endpoint'''
class Response_For_Get_All_Books(BaseModel):
    success: bool
    message: str
    books: List[AddBook]