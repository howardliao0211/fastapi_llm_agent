from database.models.chat import Chat
from database.models.user import User
from fastapi import Depends
from apis.deps import get_db, get_current_user
from sqlmodel import Session

def insert_chat(user_id:int, title:str, db:Session=Depends(get_db)) -> Chat:
    db_chat = Chat(
        user_id=user_id,
        title=title
    )

    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat
