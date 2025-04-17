from ..model import UserEntity
from ..exceptions import ExistingUserEmailException, MissingUserIdException
from ..dto import convert_user_dto
from ..config import get_password_hash
from ..request import *
from ..dto import UserDTO
from sqlmodel import select
from typing import List

class UserService:
    def create_user(self, request : CreateUserRequest, session) -> None:
        
        name = request.name
        email = request.email
        disabled = request.disabled
        plain_password = request.password
        hashed_password = get_password_hash(plain_password)

        statement = select(UserEntity).where(UserEntity.email == email)
        existing_user = session.exec(statement).first()

        if existing_user:
            raise ExistingUserEmailException(email=email)

        user_model = UserEntity(name=name, email=email, password=hashed_password, disabled=disabled)
        session.add(user_model)
        session.commit()
        session.refresh(user_model)

    def list_all_users(self, session) -> List[UserDTO]:
        statement = select(UserEntity)
        user_entity_list = session.exec(statement)
        user_dto_list = []

        if user_entity_list:
            for user_entity in user_entity_list:
                user_dto_list.append(
                    convert_user_dto(user_entity)
                )

        return user_dto_list

    def update_user(self, user_id : int, request : UpdateUserRequest, session): 

        user_model = session.get(UserEntity, user_id) 

        if not user_model:
            raise MissingUserIdException(idx=user_id)
        
        user_model.name = request.name or user_model.name
        user_model.email = request.email or user_model.email
        user_model.disabled = request.disabled or user_model.disabled

        if request.password:
            user_model.password = get_password_hash(request.password)

        session.add(user_model)
        session.commit()
        session.refresh(user_model)