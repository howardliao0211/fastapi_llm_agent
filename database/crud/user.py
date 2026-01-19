from schemas.user import UserCreate, ShowUser
from apis.deps import get_db
from fastapi import Depends
from sqlmodel import Session, select
from database.models.user import User
from typing import List

def insert_user(user: UserCreate, db:Session = Depends(get_db)) -> User:
    db_user = User(
        username=user.email,
        **user.model_dump()
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_all_users(db: Session=Depends(get_db)) -> List[User]:
    result = db.exec(select(User))
    return result.all()

def get_user_by_email(email: str, db: Session=Depends(get_db)) -> User:
    result = db.exec(select(User).where(User.email == email))
    return result.first()
