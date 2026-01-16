from fastapi import APIRouter
from apis.user import router as user_router

api_router = APIRouter()
api_router.include_router(
    router=user_router,
    tags=["users"]
)
