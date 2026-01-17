from fastapi import APIRouter, status, Depends
from schemas.chat import ChatCreate
from schemas.message import MessageCreate, ResponseMessage
from database.crud.chat import insert_chat
from database.crud.message import insert_message
from database.models.message import Role, Message
from sqlmodel import Session, select
from apis.deps import get_db
from services.llm_service import llm_service

router = APIRouter()

@router.post("/chats", status_code=status.HTTP_201_CREATED)
def create_chat(chat: ChatCreate, db:Session=Depends(get_db)):
    return insert_chat(chat, db)

@router.post("/chats/{chat_id}/messages", response_model=ResponseMessage, status_code=status.HTTP_201_CREATED)
async def create_message(
    chat_id: int,
    message: MessageCreate,
    db:Session=Depends(get_db)
):
    insert_message(chat_id, message, db)
    
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
    insert_message(chat_id, llm_response, db)

    return llm_response
