from fastapi.security import HTTPBearer
from fastapi import Request,HTTPException,status,Depends
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_session
from src.auth.utils import decode_token
from src.db.redis import token_in_blocklist
from src.auth.services import UserServices
from typing import List,Any
from src.error import PermissionDenied,InvalidToken

user_services=UserServices()
class TokenBearer(HTTPBearer):

    def __init__(self,auto_error = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request:Request)->HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        token=creds.credentials
        token_data=decode_token(token)
      #   print(creds)
        
        
        if not token_data:

            #  raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid or Expired token")
            raise InvalidToken
        
        self.verify_token_data(token_data)

        if await token_in_blocklist(token_data['jti']):
            #   raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
            #                       detail={
            #                             "error":"this token is invalid or expired",
            #                             "resolution":"Please get New Token"
            #                       })
            raise InvalidToken
        return token_data
      

#     def token_valid(self,token:str)->bool:
#             token_data=decode_token(token)
#             return True if token_data is not None else False
    
    
    
    def verify_token_data(self,token_data):
          raise NotImplementedError("Please Override this method in child class")
    

class AccessTokenBearer(TokenBearer):
       def verify_token_data(self,token_data:dict)->None:
            
            if token_data and token_data['refresh']:
                    raise HTTPException(
                          status_code=status.HTTP_403_FORBIDDEN,
                          detail='Please provide an Access token')
            
class RefreshTokenBearer(TokenBearer):
       def verify_token_data(self,token_data:dict)->None:
            
            if token_data and not token_data['refresh']:
                    raise HTTPException(
                          status_code=status.HTTP_403_FORBIDDEN,
                          detail='Please provide an Refresh token')
            

async def get_current_user(token_detail:dict=Depends(AccessTokenBearer()),
                     session:AsyncSession=Depends(get_session)):
      email=token_detail["user"]["email"]

      user=await user_services.get_user_by_email(email,session)
      return user



      
class RoleChecker():
      def __init__(self,allowed_roles:List[str])->None:
            self.allowed_roles=allowed_roles

      def __call__(self,current_user=Depends(get_current_user)) -> Any:

            if not current_user.is_verified:
                  raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Please verify your email")
            if current_user.role in self.allowed_roles:
                  return True
            # raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
            #                     detail="you are not allowed to perform this action.")
            raise PermissionDenied