from database.models.chat import Chat
from database.models.user import User
from fastapi import Depends
from apis.deps import get_db, get_current_user
from sqlmodel import Session, select
from typing import List

def insert_chat(user_id:int, title:str, db:Session=Depends(get_db)) -> Chat:
    db_chat = Chat(
        user_id=user_id,
        title=title
    )

    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def get_chat_with_user_id(user_id: int, db: Session=Depends(get_db)) -> List[Chat]:
    result = db.exec(select(Chat).where(Chat.user_id == user_id))
    return result.all()
