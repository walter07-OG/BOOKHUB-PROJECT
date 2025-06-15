'''Import the fastapi module to create an instance of an app to decorate the api endpoints'''
from fastapi import FastAPI, Depends

'''Import the the modules, containing the connection or session to the actual database.'''
from DATABASES import book_database, book_hub_users_database, favourite_book_database

'''Import the Session from the ORM to make database sessions'''
from sqlalchemy.orm import Session

'''Import the Path from fastapi to use for the path parameter validation'''
from fastapi import Path

'''Import Annotated from the typing module to use for the path param hints and validation'''
from typing import Annotated, List

#THIS PART, WE ARE GOING TO CALL ALL THE DATABASES WE HAVE ACTUALLY CREATED IN THE MODELS.
from MODELS_FOR_DATABASES import model_for_book_database, model_for_favs_database, model_for_users_database
users_database = model_for_users_database.USERS
the_book_database = model_for_book_database.Book
the_users_favourites_database = model_for_favs_database.FAVOURITE_BOOK




#THIS PART CONTAINS THE IMPORTS OF VALIDATION FILES, FOR THE REQUEST AND RESPONSE OF A REQUEST AND AN API RESPONSE
#*****
from  ENDPOINT_VALIDATIONS import get_all_books_validator
from ENDPOINT_VALIDATIONS import book_details_validator
from ENDPOINT_VALIDATIONS import add_book_validator
from ENDPOINT_VALIDATIONS import update_book_validator_with_id
from ENDPOINT_VALIDATIONS import delete_book_validator
#*****

#Definitions of functions to use as database sessions to use to access the various databases we are going to use in the API
'''SESSION FUNCTION FOR BOOKDATABASE'''
def book_database_session():
    the_session = book_database.the_session_for_books()
    try:
        yield the_session
    finally:
        the_session.close()

'''SESSION FUNCTION FOR BOOKHUB_USERS DATABASE'''
def book_hub_users_database_session():
    the_session = book_hub_users_database.the_session_for_users()
    try:
        yield the_session
    finally:
        the_session.close()

'''SESSION FUNCTION FOR FAVOURITE_BOOK_DATABASE'''
def user_favourite_database_session():
    the_session = favourite_book_database.the_session_for_favourites()
    try:
        yield the_session
    finally:
        the_session.close()


'''we create an instance of the fastapi app'''
book_app = FastAPI(docs_url = "/docs")


#The definition for all the endpoints which will be used for the API.


@book_app.get("/books", response_model = List[get_all_books_validator.Response_For_Get_All_Books])
def get_all_books(database_connection: Session = Depends(book_database_session)):
    """
    Retrieve all books from the database.

    Returns a JSON response with status, message, and a list of all books.
    Depends on a database session provided by book_database_session.
    """
    the_books_in_the_database = database_connection.query(book_database).all()
    return {
        "status": "success",
        "message": "Books retrieved successfully.",
        "data": the_books_in_the_database
    }


@book_app.get("/books/{book_id}", response_model = List[book_details_validator.Response_For_Book_Details])
def get_book_with_id(book_id: Annotated[int, Path(gt = 0, description = "Please make sure that the ID of the book is positive!")], database_connection: Session = Depends(book_database_session)):

    #Retrieve a book's details by its unique positive ID.
    #Args:
    #    book_id (int): The unique, positive identifier of the book.
    #    database_connection (Session): SQLAlchemy session dependency for database access.
    #Returns:
    #    dict: A response containing the status, message, and book data if found, or an error message if not.

    book = database_connection.query(the_book_database).filter(the_book_database.book_id == book_id).first()

    if not book:
        return {
            "status": "error",
            "message": f"Book with ID {book_id} not found.",
            "data": None
        }
    
    return {
        "status": "success",
        "message": "Book details retrieved successfully.",
        "data": book
    }

@book_app.post("/add_book", response_model = List[add_book_validator.ResponseForAddBook])
def add_books(book: add_book_validator.AddBook, database_connection: Session = Depends(book_database_session)):
    try:
        new_book = model_for_book_database.Book(**book.model_dump())
        database_connection.add(new_book)
        database_connection.commit()
        database_connection.refresh(new_book)
    except BaseException as exception:
        return {
            "error message": "Sorry there was an error in the submited model",
            "solution": "Oh! so bad for the unseccfull API call. The solution to this problem is that, 'You make sure that, the model can be changed to a json'"
        }

@book_app.put("/update_book_by_id", response_model = List[update_book_validator_with_id.UpdateBookIdResponse])
def update_book(book_to_update_info: update_book_validator_with_id.UpdateBookId, database_connection: Session = Depends(book_database_session)):
    book_to_update_id  = book_to_update_info.book_id
    book = database_connection.query(the_book_database).filter(the_book_database.book_id == book_to_update_id).first()
    for index, updated_attribute in book_to_update_info.model_dump().items():
        try:
            setattr(book, index, updated_attribute)
            database_connection.commit()
            database_connection.refresh
        except AttributeError as AE:
            return {
                "error message": f"Sorry, there was an error in updating the attribute '{index}' of the book with ID {book_to_update_id} due to an AttributeError. Please make sure that all the keys match the database fields."
            }


@book_app.delete("/delete_a_book_by_id", response_model = delete_book_validator.DeleteBookResponse)
def delete_book(book_id: delete_book_validator.DeleteBook, database_connection: Session = Depends(book_database_session)):
    book_to_delete = database_connection.query(the_book_database).filter(the_book_database.book_id == book_id).first()
    if not book_to_delete:
        return {
            "error message": f"Sorry there is no book with an id, '{book_id}'",
            "book_to_delete_info": {
                "book_id":f"{book_id}"
            },
            "success": False
        }
    database_connection.delete(book_to_delete)
    database_connection.commit()
    return {
        "message": f"You have successfully deleted the book with the ID, '{book_id}'",
        "book_deleted_info": {
            "book_id": book_to_delete.book_id,
            "book_author": book_to_delete.book_author,
            "book_title": book_to_delete.book_title,
            "book_price": book_to_delete.book_price,
            "book_genre": book_to_delete.book_genre,
            "book_year": book_to_delete.book_year,
            "book_description": book_to_delete.book_description
        }
    }
@book_app.get("/search_a_book_by_title/{book_title}")
def get_book(book_title: str, database_connection: Session = Depends(book_database_session)):
    book = database_connection.query(the_book_database).filter(the_book_database.book_title == book_title).all()
    if not book:
        return {
            "message": f"Sorry! there is no book with an ID of, '{book_title}'.",
            "book_info": f"book_id: {book_title}",
            "success": False
        }
    return {
        "message": f"You have sucessfully retrieved the book with the title, '{book_title}'.",
        "book_info": book,
        "sucess": True
    }
