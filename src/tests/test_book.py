from src.books.schemas import CreateBookModel

books_prefix = "/api/v1/books"
user_prefix= "/api/v1/user/user-login"


def test_get_all_books(test_client,fake_book_service,fake_session):
    response = test_client.get(
        url=f"{books_prefix}"
    )
    
    assert fake_book_service.get_all_books_called_once()
    assert fake_book_service.get_all_books_called_once_with(fake_session)


def test_create_book(test_client, fake_book_service, fake_session):
    book_data = {
        "title":"Test Title",
        "author" : "Test Author",
        "publisher": "Test Publications",
        "published_date":"2024-12-10",
        "language": "English",
        "page_count": 215
    }
    response = test_client.post(
        url=f"{books_prefix}",
        json=book_data
    )
    
    book_create_data = CreateBookModel(**book_data)
    assert fake_book_service.create_book_called_once()
    assert fake_book_service.create_book_called_once_with(book_create_data, fake_session)


def test_get_book_by_uid(test_client, fake_book_service,test_book, fake_session):
    response = test_client.get(f"{books_prefix}/{test_book.id}")

    assert fake_book_service.get_book_called_once()
    assert fake_book_service.get_book_called_once_with(test_book.id,fake_session)


def test_update_book_by_uid(test_client, fake_book_service,test_book, fake_session):
    response = test_client.put(f"{books_prefix}/{test_book.id}")

    assert fake_book_service.get_book_called_once()
    assert fake_book_service.get_book_called_once_with(test_book.id,fake_session)



# def test_user_login(test_client,fake_user_service,test_user,fake_session):
#     fake_user_service.user_exist.return_value = True
#     fake_user_service.get_user_by_email.return_value = test_user

#     response =test_client.post(
#         url=user_prefix,
#         json={
#             "email":test_user.email,
#             "password":test_user.password
#         }
#     )

#     fake_user_service.get_user.assert_called_once()
#     fake_user_service.get_user.assert_called_once_with(test_user.email,test_user.password,fake_session)

def test_user_login(test_client, fake_user_service, test_user, fake_session):

    from src.auth import routes

    # override service
    routes.user_services = fake_user_service

    # bypass password hashing
    routes.verify_password = lambda plain, hashed: True

    # mock responses
    fake_user_service.user_exist.return_value = True
    fake_user_service.get_user_by_email.return_value = test_user

    response = test_client.post(
        url=user_prefix,
        json={
            "email": test_user.email,
            "password": "123456"
        }
    )

    fake_user_service.user_exist.assert_called_once_with(test_user.email, fake_session)
    fake_user_service.get_user_by_email.assert_called_once_with(test_user.email, fake_session)