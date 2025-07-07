from pydantic import BaseModel
from ENDPOINT_VALIDATIONS.add_book_validator import AddBook
from typing import List

'''The validation class for get_all_books() endpoint'''
class Response_For_Get_All_Books(BaseModel):
    success: str
    api_key: str
    message: str
    books: List[AddBook]