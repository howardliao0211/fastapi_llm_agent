from schemas.chat import ChatCreate
from database.models.chat import Chat
from fastapi import Depends
from apis.deps import get_db
from sqlmodel import Session

def insert_chat(chat: ChatCreate, db:Session=Depends(get_db)) -> Chat:
    db_chat = Chat(
        **chat.model_dump()
    )

    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat
