# BookHub API

BookHub API is a RESTful service for managing books, users, and user favorites. Built with FastAPI and SQLAlchemy, it provides robust endpoints for user authentication, book CRUD operations, search, and personalized favorites management.

## Features
- User registration and authentication
- Add, update, delete, and retrieve books
- Search books by title
- Manage user-specific favorite books
- Input validation for all endpoints
- SQLAlchemy-powered database models

## Technologies Used
- Python 3.13+
- FastAPI
- SQLAlchemy
- Passlib (for password hashing)

## Getting Started

### Installation
1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd BOOKHUB_API
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
   Or, if using `pyproject.toml`:
   ```sh
   pip install .
   ```

### Running the API
```sh
uvicorn API.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

### API Documentation
Interactive docs are available at:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Project Structure
```
BOOKHUB_API/
├── API/                  # FastAPI application
├── BOOKS/                # Book-related logic
├── ENDPOINT_VALIDATIONS/ # Input validation modules
├── FAVOURITES/           # User favorites logic
├── MODELS_FOR_DATABASES/ # SQLAlchemy models
├── USERS/                # User management
├── VALIDATION_FOR_USER/  # User validation
├── main.py               # Entry point
├── pyproject.toml        # Project metadata
└── README.md             # Project documentation
```

## License
This project is licensed under the MIT License.
