from pydantic import BaseModel

'''The validation class for get_all_books() endpoint'''
class Response_For_Get_All_Books(BaseModel):
    book_id: int
    book_title: str
    book_author: str
    book_genre: str
    book_year: int
    book_price: float
    book_description: str