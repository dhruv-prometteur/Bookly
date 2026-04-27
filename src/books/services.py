from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select,desc
from src.books.schemas import CreateBookModel,UpdateBookModel
from src.db.models import Book
from uuid import UUID
from fastapi import HTTPException,status
from src.error import BookNotFound

class BookServices:
    async def get_all_books(self,session:AsyncSession):

        statement=select(Book).order_by(desc(Book.created_at))
        result=await session.execute(statement)

        books = result.scalars().all()
        return [book.model_dump() for book in books]
    async def get_all_books_by_user_uid(self,user_uid,session:AsyncSession):
        statement=select(Book).where(Book.user_uid==user_uid).order_by(desc(Book.created_at))
        result=await session.execute(statement)
        books=result.scalars().all()

        return [book.model_dump() for book in books]
    
    async def get_book(self,book_id:UUID,session:AsyncSession):
        statement=select(Book).where(Book.id==book_id)
        
        result = await session.execute(statement)
        if not result:
            # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"book with id '{book_id}' not found")
            raise BookNotFound

        book=result.scalar_one_or_none()
        # print(book)
        return book if book else None
        
    
    async def create_book(self,book_data:CreateBookModel,user_uid:str,session:AsyncSession):
        new_book=Book(**book_data.model_dump())
        new_book.user_uid=user_uid
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book.model_dump()
    
    async def update_book(self,book_id:UUID,update_data:UpdateBookModel,session:AsyncSession):

        book_to_update=await self.get_book(book_id,session)
        if book_to_update is not None:
            update_data_dict=update_data.model_dump()

            for k,v in update_data_dict.items():
                setattr(book_to_update,k,v)
            await session.commit()
            return book_to_update.model_dump()   
        else:
            return None

        # statement=select(Book).where(Book.id==book_id)
        # result = await session.exec(statement)
        # book=result.first()
        # if book:
        #     book.name=update_data_dict.get("name", book.name)
        #     book.author=update_data_dict.get("author", book.author)
        #     book.publisher=update_data_dict.get("publisher", book.publisher)
        #     book.genre=update_data_dict.get("genre", book.genre)
        #     await session.commit()
        #     await session.refresh(book)
        #     return book
        # else:
        #     return None

    async def delete_book(self,book_id:str,session:AsyncSession):
        book_to_delete=await self.get_book(book_id,session)
        print(book_to_delete)
        if book_to_delete is None:
            return False
        
        await session.delete(book_to_delete)
        await session.commit()

        return True