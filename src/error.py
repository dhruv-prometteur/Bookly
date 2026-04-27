from typing import Any,Callable
from fastapi import FastAPI,HTTPException,status
from fastapi.responses import JSONResponse
from fastapi.requests import Request
class BooklyException(Exception):
    """Base exception class for all custom Bookly application errors."""
    pass


class InvalidToken(BooklyException):
    """Raised when the provided token is invalid or has expired."""
    pass 


class InternalServerError(BooklyException):
    """Raised when an unexpected error occurs on the server."""
    pass


class BookNotFound(BooklyException):
    """Raised when a book with the given identifier does not exist."""
    pass


class UserAlreadyExists(BooklyException):
    """Raised when attempting to create a user that already exists."""
    pass


class UserNotFound(BooklyException):
    """Raised when a user with the given email or identifier is not found."""
    pass


class InvalidCredentials(BooklyException):
    """Raised when the provided login credentials are incorrect."""
    pass


class InvalidAccessToken(BooklyException):
    """Raised when the access token is invalid or expired."""
    pass


class InvalidRefreshToken(BooklyException):
    """Raised when the refresh token is invalid or expired."""
    pass


class PermissionDenied(BooklyException):
    """Raised when a user does not have permission to perform an action."""
    pass



def create_exception_handler(status_code:int,initial_detail:Any) -> Callable[[Request,Exception],JSONResponse]:

    async def exception_handler(request:Request,exc:BooklyException):
        return JSONResponse(
            content=initial_detail,
            status_code=status_code
        )
    return exception_handler



def register_all_errors(app:FastAPI):

    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message":"Token is invalid or Expired"
            }
        )
    )

    app.add_exception_handler(
        BookNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message":"Book with provided Id Not found"
            }
        )
    )
    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message":"User with provided Email Not found"
            }
        )
    )
    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            initial_detail={
                "message":"User with provided Email Already Exist"
            }
        )
    )

    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message":"Invalid Credentials"
            }
        )
    )

    app.add_exception_handler(
        InvalidAccessToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message":"invalid Access Token"
            }
        )
    )

    app.add_exception_handler(
        InvalidRefreshToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message":"Invalid Refresh Token"
            }
        )
    )

    app.add_exception_handler(
        PermissionDenied,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message":"Permission Denied"
            }
        )
    )


    app.add_exception_handler(
        InternalServerError,
        create_exception_handler(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            initial_detail={
                "message":"oops!! something went wrong!"
            }
        )
    )