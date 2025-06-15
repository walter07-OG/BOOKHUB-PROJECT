from pydantic import BaseModel

'''the validator for returning the book details using book ID'''

'''The validator for the response of the query'''
class Response_For_Book_Details(BaseModel):
    book_id: int
    book_title: str
    book_author: str
    book_genre: str
    book_year: int
    book_price: float
    book_description: str