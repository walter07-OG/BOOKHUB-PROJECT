from pydantic import BaseModel

class BookSearchResponse(BaseModel):
    message: str
    book_info: dict
    sucess: str