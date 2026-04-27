from fastapi import status,HTTPException,APIRouter,Depends

from typing import List

from src.books.schemas import Book,UpdateBookModel,BookDetailModel
from src.db.database import get_session
from src.books.services import BookServices
from sqlalchemy.ext.asyncio import AsyncSession
from src.books.schemas import CreateBookModel
from uuid import UUID
from src.auth.dependencies import AccessTokenBearer,RoleChecker
from src.error import BookNotFound


book_router=APIRouter()
book_services=BookServices()
access_token_bearer=AccessTokenBearer()
role_checker=RoleChecker(["admin","user"])


@book_router.get("/get-all-books",response_model=List[Book],dependencies=[Depends(role_checker)])
async def get_all_books(session:AsyncSession=Depends(get_session) ,user_detail=Depends(access_token_bearer) ):
    books=await book_services.get_all_books(session)
   
   
    return books

@book_router.get("/get-all-books-by-user_uid/{user_uid}",response_model=List[Book])
async def get_all_books_by_user_uid(user_uid:str,session:AsyncSession=Depends(get_session) ,user_detail=Depends(access_token_bearer) ):
    books=await book_services.get_all_books_by_user_uid(user_uid,session)

    # print(user_detail)
   
    return books

@book_router.get("/book/{book_id}",response_model=BookDetailModel)
async def get_book(book_id:UUID,session:AsyncSession=Depends(get_session),user_detail=Depends(access_token_bearer)):
    book=await book_services.get_book(book_id,session)
    if book:
        return book
    else:
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Book with id {book_id} not found")
        raise BookNotFound
  

@book_router.post("/create-book",status_code=status.HTTP_201_CREATED)
async def create_book(book_data:CreateBookModel,session:AsyncSession=Depends(get_session),token_detail=Depends(access_token_bearer))->dict:
    user_uid=token_detail.get('user')["user_uid"]
    print(token_detail)
    print(f"this is{user_uid}")
    new_book=await book_services.create_book(book_data,user_uid,session)
    return {"message":"Book created successfully","book":new_book}
  

@book_router.patch("/update-book/{book_id}")
async def update_book(book_id:UUID,book_data:UpdateBookModel,session:AsyncSession=Depends(get_session),user_detail=Depends(access_token_bearer)):
    book=await book_services.update_book(book_id,book_data,session)
    if book:
        return book
    else:
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Book with id {book_id} not found")
        raise BookNotFound

    #     if book["id"]==book_id:
    #         book["name"]=book_data.name
    #         book["author"]=book_data.author
    #         book["publisher"]=book_data.publisher
    #         book["genre"]=book_data.genre
    #         return book
    # else:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Book with id {book_id} not found")
    

@book_router.delete("/delete-book/{book_id}")
async def delete_book(book_id:str,session:AsyncSession=Depends(get_session),user_detail=Depends(access_token_bearer)):
    book=await book_services.delete_book(book_id,session)
    if book:
        return {"message":f"Book with id {book_id} deleted successfully"}
    else:
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Book with id {book_id} not found")
        raise BookNotFound
    
