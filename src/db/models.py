from sqlmodel import SQLModel,Field,Column,Relationship

from sqlalchemy.dialects import postgresql as pg

from sqlalchemy import String,DateTime

from typing import List,Optional


import uuid
from datetime import datetime,date




class User(SQLModel,table=True):
    __tablename__="users"
    uid:uuid.UUID=Field(default_factory=uuid.uuid4,primary_key=True)
  
    username:str=Field(sa_column=Column(String,nullable=False,unique=True))
    email:str=Field(sa_column=Column(String,nullable=False,unique=True))
    role:str=Field(sa_column=Column(String,nullable=False,server_default="user"))
    password:str=Field(exclude=True)
    first_name:str=Field(sa_column=Column(String,nullable=False))
    last_name:str=Field(sa_column=Column(String,nullable=False))
    is_verified:bool=Field(default=False)
    created_at:datetime=Field(sa_column=Column(DateTime,nullable=False,default=datetime.now))
    updated_at:datetime=Field(sa_column=Column(DateTime,nullable=False,default=datetime.now))

    books:List["Book"]=Relationship(back_populates="user",sa_relationship_kwargs={"lazy":"selectin"})
    reviews:List["Review"]=Relationship(back_populates="user",sa_relationship_kwargs={"lazy":"selectin"})




class Book(SQLModel,table=True):
    __tablename__="books"
    id:uuid.UUID=Field(default_factory=uuid.uuid4,primary_key=True)
    title:str
    author:str
    publisher:str
    user_uid:Optional[uuid.UUID]=Field(default=None,exclude=True,foreign_key="users.uid")
    published_date:date
    page_count:int
    language:str
    created_at:datetime=Field(sa_column=Column(DateTime,default=datetime.now))
    updated_at:datetime=Field(sa_column=Column(DateTime,default=datetime.now))
    user:Optional["User"]=Relationship(back_populates="books")
    reviews:List["Review"]=Relationship(back_populates="book",sa_relationship_kwargs={"lazy":"selectin"})
    def __repr__(self) -> str:
        return f"<BOOK {self.title}>"
    

class Review(SQLModel,table=True):
    __tablename__="reviews"
    uid:uuid.UUID=Field(default_factory=uuid.uuid4,primary_key=True)
    rating:int=Field(lt=5)
    review_text:str
    user_uid:Optional[uuid.UUID]=Field(default=None,foreign_key="users.uid")

    book_uid:Optional[uuid.UUID]=Field(default=None,foreign_key="books.id")
    created_at:datetime=Field(sa_column=Column(DateTime,default=datetime.now))
    updated_at:datetime=Field(sa_column=Column(DateTime,default=datetime.now))

    user:Optional["User"]=Relationship(back_populates="reviews")
    book:Optional["Book"]=Relationship(back_populates="reviews")


    def __repr__(self):
        return f"<Review for Book {self.book_uid} by User {self.user_uid}>"
        