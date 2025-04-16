from fastapi import APIRouter, status, Depends
from typing import Annotated
from ..utils import get_logger
from ..request import *
from ..response import BaseResponse, BaseError, UserListResponse
from ..service import user_service
from ..config import SessionDep, get_current_active_user
from ..exceptions import ExistingUserEmail
from ..model import UserEntity
from ..dto import convert_user_dto, UserDTO

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
    description="Route for creating a user",
    response_model=BaseResponse
)
async def put_user(request : CreateUserRequest, session : SessionDep) -> BaseResponse | BaseError:
    logger.info(f"{put_user.__name__} endpoint accessed")
    try:
        user_service.create_user(request, session)
    except ExistingUserEmail as e:
        logger.error(e.message)
        return BaseError(
            status=status.HTTP_400_BAD_REQUEST, 
            message=e.message
        )
    return BaseResponse()

@router.get(
    path="/api/user/me",
    tags=['User API'],
    response_model=UserDTO
)
async def read_user_me(current_user: Annotated[UserEntity, Depends(get_current_active_user)],) -> UserDTO:
    return convert_user_dto(current_user)