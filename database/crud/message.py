from schemas.message import MessageCreate
from fastapi import Depends
from sqlmodel import Session
from apis.deps import get_db
from database.models.message import Message

def insert_message(chat_id: int, message: MessageCreate, db: Session=Depends(get_db)) -> Message:
    db_msg = Message(
        chat_id=chat_id,
        **message.model_dump()
    )

    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)
    return db_msg
