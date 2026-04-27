from src.auth.schemas import CreateUserModel
from fastapi import Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_session
from src.db.models import User
from src.auth.utils import hash_password,verify_password

class UserServices:
   
    
    async def get_user_by_email(self,email:str,session:AsyncSession):
        statement=select(User).where(User.email==email)
        result=await session.execute(statement)
        user=result.scalar_one_or_none()
        return user
    
    async def user_exist(self,email:str,session:AsyncSession):
        user=await self.get_user_by_email(email,session)

        if user is not None:
            return True
        else:
            return False
        
    async def create_user(self,user_data:CreateUserModel,session:AsyncSession):
        data=user_data.model_dump()
        data["password"]=hash_password(data["password"])
        new_user=User(**data)

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user.model_dump() 
    
    async def update_user(self,user:User,user_data:dict,session:AsyncSession=Depends(get_session)):
        
        for k,v in user_data.items():
            setattr(user,k,v)
        await session.commit()

        return user

       

