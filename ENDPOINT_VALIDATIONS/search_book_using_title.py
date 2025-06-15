from pydantic import BaseModel

class BookSearch(BaseModel):
    book_title: str

class BookSearchResponse:
    message: str
    book_info: dict
    sucess: str