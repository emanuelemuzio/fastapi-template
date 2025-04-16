from pydantic import BaseModel

class CreateUserRequest(BaseModel):
    name : str = 'Full Name'
    email : str = 'example@mail.com'
    password : str = 'password'
    disabled : bool = False