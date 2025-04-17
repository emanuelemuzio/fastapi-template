from pydantic import BaseModel
from ..model import UserEntity

class UserDTO(BaseModel):
    id : int
    name : str
    email : str

def convert_user_dto(model : UserEntity) -> UserDTO:
    dto = UserDTO(id=model.id, name=model.name, email=model.email)
    return dto