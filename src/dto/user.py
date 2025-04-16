from pydantic import BaseModel
from ..model import UserEntity

class UserDTO(BaseModel):
    name : str
    email : str

def convert_user_dto(model : UserEntity) -> UserDTO:
    dto = UserDTO(name=model.name, email=model.email)
    return dto