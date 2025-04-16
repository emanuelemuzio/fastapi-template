from pydantic import BaseModel

class BaseError(BaseModel):
    status : int = 500
    message : str = "Operazione fallita"