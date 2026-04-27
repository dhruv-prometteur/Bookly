from typing import Optional
from pydantic import BaseModel
import uuid
from datetime import datetime


class ReviewModel(BaseModel):
    uid:uuid.UUID
    rating:int
    review_text:str
    book_uid:Optional[uuid.UUID]
    user_uid:Optional[uuid.UUID]
    created_at:datetime
    updated_at:datetime

class CreateReviewModel(BaseModel):
    rating:int
    review_text:str



