'''Import the fastapi module to create an instance of an app to decorate the api endpoints'''
from fastapi import APIRouter, Depends, Query

'''Import the the modules, containing the connection or session to the actual database.'''
from MODELS_FOR_DATABASES.book_database import the_session_for_books

'''Import the Session from the ORM to make database sessions'''
from sqlalchemy.orm import Session

'''Import the Path from fastapi to use for the path parameter validation'''
from fastapi import Path

'''Import Annotated from the typing module to use for the path param hints and validation'''
from typing import Annotated, List

#THIS PART, WE ARE GOING TO CALL ALL THE DATABASES WE HAVE ACTUALLY CREATED IN THE MODELS.
from MODELS_FOR_DATABASES import model_for_book_database 
the_book_database = model_for_book_database.Book




#THIS PART CONTAINS THE IMPORTS OF VALIDATION FILES, FOR THE REQUEST AND RESPONSE OF A REQUEST AND AN API RESPONSE
#*****
from .VALIDATION_FOR_BOOKS import get_all_books_validator
from .VALIDATION_FOR_BOOKS import book_details_validator
from .VALIDATION_FOR_BOOKS import add_book_validator
from .VALIDATION_FOR_BOOKS import update_book_validator
from .VALIDATION_FOR_BOOKS import delete_book_validator
from .VALIDATION_FOR_BOOKS import get_books_response
#*****

#Definitions of functions to use as database sessions to use to access the various databases we are going to use in the API
'''SESSION FUNCTION FOR BOOKDATABASE'''
def book_database_session():
    the_session = the_session_for_books()
    try:
        yield the_session
    finally:
        the_session.close()




'''we create an instance of the fastapi app'''
books_router = APIRouter()

#The definition for all the endpoints which will be used for the API.




'''THESE ENDPOINTS ARE THE CORE(RESTFUL) BOOK API ENDPOINTS'''

@books_router.get("/books", response_model = List[get_all_books_validator.Response_For_Get_All_Books], tags = ["Search Book"])
def get_all_books(database_connection: Session = Depends(book_database_session)):
    """
    Retrieve all books from the database.

    Returns a JSON response with status, message, and a list of all books.
    Depends on a database session provided by book_database_session.
    """
    the_books_in_the_database = database_connection.query(the_book_database).all()
    return [
        {
        "success": "True",
        "message": "Books retrieved successfully.",
        "books": the_books_in_the_database
    }
    ]


@books_router.get("/books/{book_id}", response_model = List[book_details_validator.Response_For_Book_Details], tags = ["Search Book"])
def get_book_with_id(book_id: Annotated[int, Path(gt = 0, description = "Please make sure that the ID of the book is positive!")], database_connection: Session = Depends(book_database_session)):

    #Retrieve a book's details by its unique positive ID.
    #Args:
    #    book_id (int): The unique, positive identifier of the book.
    #    database_connection (Session): SQLAlchemy session dependency for database access.
    #Returns:
    #    dict: A response containing the status, message, and book data if found, or an error message if not.

    book = database_connection.query(the_book_database).filter(the_book_database.book_id == book_id).first()

    if not book:
        return [
            {
            "status": "error",
            "message": f"Book with ID {book_id} not found.",
            "data": None
        }
        ]
    
    return [
        {
        "status": "success",
        "message": "Book details retrieved successfully.",
        "data": book
    }
    ]

@books_router.post("/add_book", response_model = List[add_book_validator.ResponseForAddBook], tags = ["Add Book"])
def add_books(book: add_book_validator.AddBook, database_connection: Session = Depends(book_database_session)):
    try:
        search_book = database_connection.query(the_book_database).filter(the_book_database.book_id == book.book_id).first()
        if search_book:
            return [
                {
                    "success": False,
                    "message": "Sorry it seems the book already exists!",
                    "book": {
                        "book_id": search_book.book_id,
                        "book_title": search_book.book_title,
                        "book_author": search_book.book_author,
                        "book_genre": search_book.book_genre,
                        "book_year": search_book.book_year,
                        "book_price": search_book.book_price,
                        "book_description": search_book.book_description
                    }
                    
                }
            ]
        new_book = model_for_book_database.Book(**book.model_dump())
        database_connection.add(new_book)
        database_connection.commit()
        database_connection.refresh(new_book)
        return [
            {
            "success": True,
            "message": "Book added successfully.",
            "book": {
                "book_id": book.book_id,
                "book_title": book.book_title,
                "book_author": book.book_author,
                "book_genre": book.book_genre,
                "book_year": book.book_year,
                "book_price": book.book_price,
                "book_description": book.book_description
            }
            }
        ]
    except BaseException as exception:
        return [
            {
            "success": False,
            "message": f"Sorry there was an error in the submited model. The solution to this problem is that,  make sure  the model can be changed to a json {exception}",
            "book": {}
        }

        ]
@books_router.put("/update_book/{book_id}", response_model = List[update_book_validator.UpdateBookIdResponse], tags = ["Update Book"])
def update_book(book_id: Annotated[int, Path(gt = 0, description = "Please make sure that the ID of the book is positive!")], Book_to_update_info: update_book_validator.UpdateBookId, database_connection: Session = Depends(book_database_session)):
    book = database_connection.query(the_book_database).filter(the_book_database.book_id == book_id).first()
    if book:
        # Only update fields provided by the user
        book_updates =  Book_to_update_info.model_dump(exclude_unset = True)
        for key, value in book_updates.items():
            try:
                        
                setattr(book, key, value)
            except (TypeError, ValueError, AttributeError) as TV_error:
                    return [
                        {
                            "message": f"Sorry, there was an error in updating the attribute '{key}' of the book with ID {book_id} due to a ValueError, Attribute error or TypeError. Please make sure that all the values of the keys are in the expected type.",
                            "success": False,
                            "code": 500,
                        }
                    ]
        database_connection.commit()
        database_connection.refresh(book)
        return [
            {
                "message": f"You have successfully updated the book, with the ID of '{book_id}'",
                "success": True,
                "code": 200,
            }
        ]
    else:
        return [
            {
                "message": f"Sorry, there was an error in updating the book with ID, '{book_id}'. There is no book with such ID. We suppose you create a new book with that ID or You update the ID first before updating anything else.",
                "success": False,
                "code": 500,
            }
        ]
                    
                
    
    



@books_router.delete("/delete_ book_id", response_model = List[delete_book_validator.DeleteBookResponse], tags = ["Delete Book"])
def delete_book(book_to_delete_info: delete_book_validator.DeleteBook, database_connection: Session = Depends(book_database_session)):
    book_to_delete = database_connection.query(the_book_database).filter(the_book_database.book_id == book_to_delete_info.book_id).first()
    if not book_to_delete:
        return [
        {
        "message": f"You have  failed to update the book with an ID of '{book_to_delete_info.book_id}'",
        "book_deleted_info": {
            "book_id": book_to_delete_info.book_id,
            
        },
        "success": False
        }
    ]
            
            
    
    database_connection.delete(book_to_delete)
    database_connection.commit()
    database_connection.refresh
    return [
        {
        "message": f"You have successfully deleted the book with an ID of '{book_to_delete_info.book_id}'",
        "book_deleted_info": {
            "book_id": book_to_delete.book_id,
            "book_title": book_to_delete.book_title,
            "book_author": book_to_delete.book_author,
            "book_genre": book_to_delete.book_genre,
            "book_year": book_to_delete.book_year,
            "book_price": book_to_delete.book_price,
            "book_description": book_to_delete.book_description
        },
        "success": True    
        }
    ]





'''THESE ENDPOINTS ARE FOR SEARCH AND FILTERS OF BOOKS IN THE DATABASE.'''

@books_router.get("/search_a_book_by_title/{book_title}", tags = ["Search Book"], response_model = List[get_books_response.BookSearchResponse])
def get_book_with_title(book_title: str, database_connection: Session = Depends(book_database_session)):
    book = database_connection.query(the_book_database).filter(the_book_database.book_title == book_title).first()
    if not book:
        return [
            {
            "message": f"Sorry! there is no book with a title of '{book_title}'.",
            "book_info": {
            "book_id": 1,  # Changed from 0 to meet gt=0 validation
            "book_title": "",
            "book_author": "",
            "book_genre": "",
            "book_year": 1000,  # Changed from 0 to meet ge=1000 validation
            "book_price": 0.0,
            "book_description": ""
            },
            "success": True
        }
        ]
    
    return [
        {
        "message": f"You have sucessfully retrieved the book with the title, '{book_title}'.",
        "book_info": {
            "book_id": book.book_id,
            "book_title": book.book_title,
            "book_author": book.book_author,
            "book_genre": book.book_genre,
            "book_year": book.book_year,
            "book_price": book.book_price,
            "book_description": book.book_description
        },
        "success": True
    }
    ]


@books_router.get("/search_book_by_author", tags=["Search Book"], response_model=List[get_books_response.BookSearchResponse])
def get_books_by_author(
    author_name: str = Query(..., description="Name of the author to search for"),
    database_connection: Session = Depends(book_database_session)
):
    books = database_connection.query(the_book_database).filter(the_book_database.book_author.ilike(f"%{author_name}%"))

    if not books:
        return [
            {
                "message": f"Sorry! There are no books by author '{author_name}'.",
                "book_info": {
                    "book_id": 1,
                    "book_title": "",
                    "book_author": "",
                    "book_genre": "",
                    "book_year": 1000,
                    "book_price": 0.0,
                    "book_description": ""
                },
                "success": False
            }
        ]
    
    return [
        {
            "message": f"You have successfully retrieved books by author '{author_name}'.",
            "book_info": {
                "book_id": book.book_id,
                "book_title": book.book_title,
                "book_author": book.book_author,
                "book_genre": book.book_genre,
                "book_year": book.book_year,
                "book_price": book.book_price,
                "book_description": book.book_description
            },
            "success": True
        }
        for book in books
    ]