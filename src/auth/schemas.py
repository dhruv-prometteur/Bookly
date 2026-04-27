from pydantic import BaseModel,Field
from uuid import UUID
from datetime import datetime
from typing import List
from src.db.models import Book
from src.review.schemas import ReviewModel


class CreateUserModel(BaseModel):
    username:str=Field(max_length=15)
    email:str=Field(max_length=40)
    password:str=Field(min_length=6)
    role:str="user"
    first_name:str
    last_name:str

class UserLoginModel(BaseModel):
    email:str
    password:str

class UserResponseModel(BaseModel):
    uid:UUID
    username:str
    email:str
    role:str
    first_name:str
    last_name:str
    is_verified:bool
    created_at:datetime
    updated_at:datetime
    books:List[Book]
    reviews:List[ReviewModel]

class SendEmailModel(BaseModel):
    addresses:List[str]
    subject:str
    body:str


class PasswordResetRequestModel(BaseModel):
    email:str

class ResetPasswordModel(BaseModel):
    new_password:str
    confirm_password:str
