from pydantic import BaseModel, Field, field_validator
from datetime import datetime

current_year = datetime.now().year
'''Definition of the class to validate the POST request made to validate the creation of a new book'''

class AddBook(BaseModel):
    book_id: str | int | float
    book_title: str
    book_author: str
    book_genre: str
    book_year: int = Field(ge=1000, le=current_year)
    book_price: float = Field(gt = 0)
    book_description: str

    @field_validator('book_title', 'book_author', 'book_genre', 'book_description')
    @classmethod
    def all_to_lower(cls, v):
        try:
            return v.lower() if isinstance(v, str) else v
        except (ValueError, TypeError) as v_type:
            return {
                "error message": "Sorry, there was a problem in parsing some of the field inputs, into lower case.",
                "suggested solution": "Please, make sure that, the string datatypes are actually 'string datatypes' and are convertible to lower case..eg(A,b,c...Z)"
            }

'''Definition of class to validate the output to the user after the book has been added to the database.'''
class ResponseForAddBook(BaseModel):
    book: dict
    message: dict