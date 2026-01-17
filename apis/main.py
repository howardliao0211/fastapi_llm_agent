from fastapi import APIRouter
from apis.v1.user import router as user_router
from apis.v1.chat import router as chat_router

api_router = APIRouter()
api_router.include_router(
    router=user_router,
    prefix="/api/v1",
    tags=["users"]
)
api_router.include_router(
    router=chat_router,
    prefix="/api/v1",
    tags=["chats"]
)
