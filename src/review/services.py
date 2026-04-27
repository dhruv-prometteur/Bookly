from fastapi import Depends,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import Review
from src.review.schemas import CreateReviewModel
from src.books.services import BookServices
from src.auth.services import UserServices
from uuid import UUID
from src.error import InternalServerError,BookNotFound

book_service=BookServices()
user_service=UserServices()

class ReviewService:
    

    async def add_review_to_book(self,user_email:str,book_uid:UUID,review_data:CreateReviewModel,session:AsyncSession):

        try:
            user=await user_service.get_user_by_email(user_email,session)
            book=await book_service.get_book(book_uid,session)

            if not book:
                # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"book with id '{book_uid}' Not Found")
                raise BookNotFound
        
            review=Review(**review_data.model_dump())


            
        
            review.book=book
            review.use=user

            session.add(review)
            await session.commit()
            await session.refresh(review)

            return review
        except Exception as e:
            raise InternalServerError
            # raise HTTPException(
            #     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            #     detail="Oops Something Went Wrong!!")
        


    