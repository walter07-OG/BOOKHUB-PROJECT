import unittest
from fastapi.testclient import TestClient
from API.main import book_api
from MODELS_FOR_DATABASES.book_database import the_session_for_books
from MODELS_FOR_DATABASES.model_for_book_database import Book, Base
from MODELS_FOR_DATABASES.book_database import the_engine

class TestAddBookEndpoint(unittest.TestCase):
    def setUp(self):
        # Create test client
        self.client = TestClient(book_api)
        
        # Create tables before each test
        Base.metadata.create_all(bind=the_engine)
        
        # Sample valid book data
        self.valid_book = {
            "book_id": 1,
            "book_title": "Test Book",
            "book_author": "Test Author",
            "book_genre": "Test Genre",
            "book_year": 2026,
            "book_price": 29.99,
            "book_description": "Test description"
        }
        
        # Sample invalid book data
        self.invalid_book = {
            "book_id": -1,  # Invalid ID (must be > 0)
            "book_title": "Test Book",
            "book_author": "Test Author",
            "book_genre": "Test Genre",
            "book_year": 3000,  # Invalid year (must be <= current year)
            "book_price": -10,  # Invalid price (must be > -1)
            "book_description": "Test description"
        }

    def tearDown(self):
        # Clean up the database after each test
        session = the_session_for_books()
        session.query(Book).delete()
        session.commit()
        session.close()

    def test_add_valid_book(self):
        """Test adding a valid book"""
        response = self.client.post("/book/add_book", json=self.valid_book)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(len(data), 1)  # Response should be a list with one item
        response_data = data[0]
        
        self.assertTrue(response_data["success"])
        self.assertEqual(response_data["message"], "Book added successfully.")
        self.assertEqual(response_data["book"]["book_id"], self.valid_book["book_id"])
        self.assertEqual(response_data["book"]["book_title"], self.valid_book["book_title"].lower())

    def test_add_duplicate_book(self):
        """Test adding a book with duplicate ID"""
        # First add a book
        self.client.post("/book/add_book", json=self.valid_book)
        
        # Try to add the same book again
        response = self.client.post("/book/add_book", json=self.valid_book)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        response_data = data[0]
        self.assertFalse(response_data["success"])
        self.assertEqual(response_data["message"], "Sorry it seems the book already exists!")

    def test_add_invalid_book(self):
        """Test adding a book with invalid data"""
        response = self.client.post("/book/add_book", json=self.invalid_book)
        self.assertEqual(response.status_code, 422)  # Validation error

    def test_add_book_with_missing_fields(self):
        """Test adding a book with missing required fields"""
        incomplete_book = {
            "book_id": 1,
            "book_title": "Test Book"
            # Missing other required fields
        }
        response = self.client.post("/book/add_book", json=incomplete_book)
        self.assertEqual(response.status_code, 422)  # Validation error

    def test_add_book_with_invalid_price_range(self):
        """Test adding a book with price outside valid range"""
        book_with_invalid_price = self.valid_book.copy()
        book_with_invalid_price["book_price"] = 1000001  # Price must be <= 1000000
        
        response = self.client.post("/book/add_book", json=book_with_invalid_price)
        self.assertEqual(response.status_code, 422)  # Validation error

if __name__ == '__main__':
    unittest.main()
