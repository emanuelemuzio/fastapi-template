from pydantic import BaseModel
from ..config.constants import BASE_STATUS, BASE_MESSAGE

class BaseResponse(BaseModel):
    status : int = BASE_STATUS
    message : str = BASE_MESSAGE 
    data : dict = {}