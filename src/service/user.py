from ..model import UserEntity
from sqlmodel import select
from ..exceptions import ExistingUserEmail
from ..dto import convert_user_dto
from ..config import get_password_hash

class UserService:
    def create_user(self, request, session):
        
        name = request.name
        email = request.email
        disabled = request.disabled
        plain_password = request.password
        hashed_password = get_password_hash(plain_password)

        statement = select(UserEntity).where(UserEntity.email == email)
        existing_user = session.exec(statement).first()

        if existing_user:
            raise ExistingUserEmail(email=email)

        user_model = UserEntity(name=name, email=email, password=hashed_password, disabled=disabled)
        session.add(user_model)
        session.commit()

    def list_all_users(self, session):
        statement = select(UserEntity)
        user_entity_list = session.exec(statement)
        user_dto_list = []

        if user_entity_list:
            for user_entity in user_entity_list:
                user_dto_list.append(
                    convert_user_dto(user_entity)
                )

        return user_dto_list