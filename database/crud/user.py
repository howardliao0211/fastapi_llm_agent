from schemas.user import UserCreate, ShowUser
from apis.deps import get_db
from fastapi import Depends
from sqlmodel import Session
from database.models.user import User

def insert_user(user: UserCreate, db:Session = Depends(get_db)) -> User:
    db_user = User(
        username=user.email,
        **user.model_dump()
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user