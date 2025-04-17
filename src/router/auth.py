from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta
from ..utils import get_logger
from ..request import *
from ..response import BaseResponse, BaseError, UserListResponse
from ..service import user_service
from ..config import SessionDep, Token, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from ..exceptions import ExistingUserEmailException

router = APIRouter()
logger=get_logger()

@router.get(
    path="/api/user/all", 
    tags=['User API'],
    description="Route for getting info about the current active user"
)
async def user_all(session : SessionDep) -> UserListResponse | BaseError:
    logger.info(f"{user_all.__name__} endpoint accessed")
    try:
        user_list = user_service.list_all_users(session)
        return UserListResponse(
            user_list=user_list
        )
    except Exception as e:
        return BaseError(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            message=e.message
        )
    

@router.put(
    path="/api/user", 
    tags=['User API'],
    description="Route for creating a user"
)
async def put_user(request : CreateUserRequest, session : SessionDep) -> BaseResponse | BaseError:
    logger.info(f"{put_user.__name__} endpoint accessed")
    try:
        user_service.create_user(request, session)
    except ExistingUserEmailException as e:
        logger.error(e.message)
        return BaseError(
            status=status.HTTP_400_BAD_REQUEST, 
            message=e.message
        )
    return BaseResponse()

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session : SessionDep
) -> Token:
    logger.info(f"{login_for_access_token.__name__} endpoint accessed")
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")