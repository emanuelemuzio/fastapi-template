from .user import router as user_router
from .auth import router as auth_router

routers = [
    user_router,
    auth_router
]