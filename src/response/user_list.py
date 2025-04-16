from .base import BaseResponse
from ..config.constants import BASE_STATUS, BASE_MESSAGE
from typing import List
from ..dto import UserDTO

class UserListResponse(BaseResponse):
    data : dict = {}

    def __init__(self, user_list : List[UserDTO], status=BASE_STATUS, message=BASE_MESSAGE):
        super().__init__(status=status, message=message)
        self.data['user_list'] = user_list