from fastapi import APIRouter, status, Depends
from schemas.user import UserCreate, ShowUser
from apis.deps import get_db
from database.models.user import User
from database.crud.user import insert_user
from sqlmodel import Session

router = APIRouter()

@router.post("/users", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session=Depends(get_db)):
    return insert_user(user, db)
