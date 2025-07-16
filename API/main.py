from fastapi import FastAPI
"""
main.py
This module initializes the FastAPI application for the BookHub API and includes the books router.
Modules:
    - FastAPI: The web framework used to build the API.
    - books_router: The router containing all endpoints related to book operations, imported from BOOKS.books.
Attributes:
    book_api (FastAPI): The main FastAPI application instance for the BookHub API.
Routes:
    /book: All endpoints related to book management are prefixed with '/book'.
Usage:
    Run this module to start the BookHub API server. The API will expose all book-related endpoints under the '/book' path.
Example:
    uvicorn API.main:book_api --reload
"""

from USERS.users import user_router

from BOOKS.books import books_router

book_api = FastAPI(title="BOOKHUB API ENDPOINTS", version="1.0.0")
book_api.include_router(books_router, prefix = "/book")
book_api.include_router(user_router, prefix="/user")