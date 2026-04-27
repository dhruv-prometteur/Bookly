from fastapi import APIRouter,Depends,HTTPException,status,BackgroundTasks
from src.auth.schemas import CreateUserModel,UserLoginModel,UserResponseModel,SendEmailModel,PasswordResetRequestModel,ResetPasswordModel
from src.db.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.services import UserServices
from src.auth.utils import create_access_token,decode_token,verify_password,create_url_safe_token,decode_url_safe_token,hash_password
from datetime import timedelta,datetime
from fastapi.responses import JSONResponse
from src.auth.dependencies import RefreshTokenBearer, AccessTokenBearer,get_current_user,RoleChecker
from src.db.redis import add_jti_to_blocklist
from src.books.schemas import CreateBookModel
from src.error import UserAlreadyExists,UserNotFound,InvalidAccessToken,InvalidCredentials,InvalidRefreshToken,InvalidToken
from src.mail import mail,create_message
from src.config import Config
from src.celery_task import send_mail

user_router=APIRouter()
user_services=UserServices()
role_checker=RoleChecker(["admin","user"])

REFRESH_TOKEN_EXPIRY=2

@user_router.post("/send-mail")
async def send_mail(mail_data:SendEmailModel,bg_task:BackgroundTasks):
    emails=mail_data.addresses
    subject=mail_data.subject
    body=mail_data.body
    
    send_mail.delay(emails,subject,body)
    # message=create_message(emails,subject,body)

    # bg_task.add_task(mail.send_message,message)

    return f"mail sent successfully to {emails}"


@user_router.post("/user-signup")
async def user_signup(user_data:CreateUserModel,session:AsyncSession=Depends(get_session)):
    email=user_data.email
    user=await user_services.user_exist(email,session)
    if user:
        # raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user with email '{email}' already exist.")
        raise UserAlreadyExists
    new_user=await user_services.create_user(user_data,session)
    token=create_url_safe_token({"email": email})
    link=f"http://{Config.DOMAIN}/api/v1/user/verify/{token}"
    subject="Verfication Mail"
    body=f"""
<h1> Verification Mail</h1>
<p>Please Click The Below link to Verify.</p>
<a href="{link}">link</a>
"""
    message=create_message([email],subject,body)

    await mail.send_message(message)



    return {

        "message": "Account Created! Please Check Your Email TO Verify Account",
        "user":new_user
    }

@user_router.post("/user-login")
async def user_login(login_data:UserLoginModel,session:AsyncSession=Depends(get_session)):
    email=login_data.email
    password=login_data.password

    exist=await user_services.user_exist(email,session)
    if not exist:
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with email '{email}' Not Found")
        raise UserNotFound
    user = await user_services.get_user_by_email(email,session)

    if user is not None:
        password_valid=verify_password(password,user.password)
        if password_valid:
            access_token=create_access_token(
                user_data={
                    "email":user.email,
                    'user_uid':str(user.uid),
                    "user_role":user.role
                }
            )

            refresh_token=create_access_token(
                user_data={
                    "email":user.email,
                    "user_uid":str(user.uid)
                },
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
                refresh=True
            )
            
            return JSONResponse(
                content={
                    "message":"Login Successfull",
                    "access_token":access_token,
                    "refresh_token":refresh_token,
                    "user":{
                        "email":user.email,
                        "uid":str(user.uid)
                           }
                        }
            )



    
    # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Credentials")
    raise InvalidCredentials

@user_router.get("/verify/{token}")
async def verify_email(token:str,session:AsyncSession=Depends(get_session)):

    token_data=decode_url_safe_token(token)
    if token_data:
        user_email = token_data["email"]
        user=await user_services.get_user_by_email(user_email,session)
        if not user:
            raise UserNotFound()
        await user_services.update_user(user,{"is_verified":True},session)

        return JSONResponse(
            content={ "message":"Account Verified Successfully."},
            status_code=status.HTTP_200_OK
        )
    
    return JSONResponse(
        content={"message":"Error Occured During Verification"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )



    
@user_router.get("/me",response_model=UserResponseModel)
async def get_current_user(user=Depends(get_current_user),_:bool=Depends(role_checker)):
    return user


@user_router.get("/refresh-token")
async def get_new_access_token(token_details:dict=Depends(RefreshTokenBearer())):
    expiry_timesatmp=token_details["exp"]

    if datetime.fromtimestamp(expiry_timesatmp) >datetime.now():
        new_access_token=create_access_token(
            user_data=token_details["user"]
        )
        return JSONResponse(content={"access_token":new_access_token})
    # raise HTTPException(
    #     status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid Or Expired Token"
    # )
    raise InvalidRefreshToken
    

@user_router.get("/user-logout")
async def revoke_token(token_details:dict=Depends(AccessTokenBearer())):
    jti=token_details['jti']

    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={
            "message":"Logged Out Successfully"
        },
        status_code=status.HTTP_200_OK
    )



@user_router.post("/password-reset-request")
async def password_reset_request(email_data:PasswordResetRequestModel):
    email=email_data.email
    
    token=create_url_safe_token({"email": email})
    link=f"http://{Config.DOMAIN}/api/v1/user/reset-password/{token}"
    subject="Reset Your Password"
    body=f"""
<h1> reset your Password</h1>
<p>Please Click The Below link to Reset Your Password.</p>
<a href="{link}">link</a>
"""
    message=create_message([email],subject,body)

    await mail.send_message(message)

    return JSONResponse(
        content={"message":"Please Check your Mail to Reset Your Password"},
        status_code=status.HTTP_200_OK
    )


@user_router.post("/reset-password/{token}")
async def reset_password(token:str,password_data:ResetPasswordModel,session:AsyncSession=Depends(get_session)):
    token_data=decode_url_safe_token(token)
    user_email=token_data["email"]

    if user_email:
        user=await user_services.get_user_by_email(user_email,session)
        
        if user:
            new_password=password_data.new_password
            confirm_password=password_data.confirm_password
            if new_password != confirm_password:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="new password and confirm password should be same.")
            hash_pass=hash_password(new_password)
            await user_services.update_user(user,{"password":hash_pass},session)

            return JSONResponse(
                content={"message":"password changed successfully."},
                status_code=status.HTTP_200_OK
            )
        raise UserNotFound()
    raise JSONResponse(
        content={"message":"An error Occured During the ResetPassword"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


