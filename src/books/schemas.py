from datetime import datetime,date
import uuid
from typing import List
from pydantic import BaseModel
from src.review.schemas import ReviewModel


class Book(BaseModel):
    id:uuid.UUID
    title:str
    author:str
    publisher:str
    published_date:date
    page_count:int
    language:str
    created_at:datetime
    updated_at:datetime

class BookDetailModel(Book):
    reviews:List[ReviewModel]


class CreateBookModel(BaseModel):
    title:str
    author:str
    publisher:str
    published_date:date
    page_count:int
    language:str
   
    

   

class UpdateBookModel(BaseModel):
    title:str
    author:str
    publisher:str
    published_date:str
    page_count:int
    language:str
    