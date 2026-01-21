from schemas.message import MessageCreate
from fastapi import Depends
from sqlmodel import Session, select
from apis.deps import get_db
from database.models.message import Message, Role
from services.llm_service import llm_service

def insert_message(chat_id: int, message: MessageCreate, db: Session=Depends(get_db)) -> Message:
    db_msg = Message(
        chat_id=chat_id,
        **message.model_dump()
    )

    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)
    return db_msg

async def handle_llm_turn(chat_id: int, new_message: MessageCreate, db: Session=Depends(get_db)) -> Message:
    insert_message(chat_id, new_message, db)

    # Load chat history
    history = db.exec(
        select(Message).where(Message.chat_id == chat_id).order_by(Message.created_at.asc())
    ).all()

    messages = [
        {"role": msg.role.value, "content": msg.content}
        for msg in history
    ]

    llm_response = await llm_service.call_chat_completion(
        messages=messages
    )

    llm_response = MessageCreate(
        role=Role.ASSISTANT,
        content=llm_response
    )
    llm_message = insert_message(chat_id, llm_response, db)

    return llm_message
