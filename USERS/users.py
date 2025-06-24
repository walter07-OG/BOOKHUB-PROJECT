from DATABASES import book_hub_users_database


'''SESSION FUNCTION FOR BOOKHUB_USERS DATABASE'''
def book_hub_users_database_session():
    the_session = book_hub_users_database.the_session_for_users()
    try:
        yield the_session
    finally:
        the_session.close()