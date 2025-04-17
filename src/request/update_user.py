from pydantic import BaseModel

class UpdateUserRequest(BaseModel):
    name : str | None = None
    email : str | None = None
    password : str | None = None
    disabled : bool | None = None