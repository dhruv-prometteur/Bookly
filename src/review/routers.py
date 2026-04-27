from fastapi import APIRouter,Depends
from src.review.services import ReviewService
from src.db.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.review.schemas import CreateReviewModel
from src.db.models import User
from src.auth.dependencies import get_current_user
from uuid import UUID

review_router=APIRouter()


review_service=ReviewService()

@review_router.post("/add-review/{book_uid}")
async def add_review(book_uid:UUID,review_data:CreateReviewModel,current_user:User=Depends(get_current_user),session:AsyncSession=Depends(get_session)):
    email=current_user.email
    new_review=await review_service.add_review_to_book(email,book_uid,review_data,session)
    
    return new_review