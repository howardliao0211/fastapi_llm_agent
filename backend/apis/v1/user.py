from fastapi import APIRouter, status, Depends
from backend.schemas.user import UserCreate, ShowUser
from backend.apis.deps import get_db
from backend.database.models.user import User
from backend.database.crud.user import insert_user, get_all_users
from sqlmodel import Session
from typing import List

router = APIRouter()


@router.post("/users", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return insert_user(user, db)


@router.get("/users", response_model=List[ShowUser], status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):
    return get_all_users(db)
