from DATABASES import favourite_book_database


'''SESSION FUNCTION FOR FAVOURITE_BOOK_DATABASE'''
def user_favourite_database_session():
    the_session = favourite_book_database.the_session_for_favourites()
    try:
        yield the_session
    finally:
        the_session.close()