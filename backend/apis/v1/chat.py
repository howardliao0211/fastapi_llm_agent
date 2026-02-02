from fastapi import APIRouter, status, Depends
from backend.schemas.message import MessageCreate, ShowMessage
from backend.schemas.chat import ShowChat
from backend.database.crud.chat import insert_chat, get_chat_with_user_id
from backend.database.crud.message import insert_message, handle_llm_turn, get_all_messages_with_chat_id
from backend.database.models.user import User
from backend.database.models.message import Role, Message
from backend.database.models.chat import Chat
from sqlmodel import Session
from backend.apis.deps import get_db, get_current_user
from backend.services.llm_service import llm_service
from fastapi import HTTPException
from typing import List

router = APIRouter()

@router.post("/chats", response_model=ShowChat, status_code=status.HTTP_201_CREATED)
async def create_chat_with_message(
    message: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Create title from first message
    title = await llm_service.generate_title(message.content)

    # Insert chat row
    chat = insert_chat(current_user.id, title, db)

    # Process full LLM turn (user → assistant)
    response_message = await handle_llm_turn(chat.id, message, db)
    
    return chat

@router.get("/chats", response_model=List[ShowChat], status_code=status.HTTP_200_OK)
def get_chat_with_user(user: User=Depends(get_current_user), db: Session=Depends(get_db)):
    return get_chat_with_user_id(user.id, db)

@router.post("/chats/{chat_id}/messages", response_model=ShowMessage, status_code=status.HTTP_201_CREATED)
async def create_message(
    chat_id: int,
    message: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Confirm chat exists & belongs to user
    chat = db.get(Chat, chat_id)
    if not chat or chat.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    response_message = await handle_llm_turn(chat.id, message, db)
    return response_message

@router.get("/chats/{chat_id}/messages", response_model=List[ShowMessage], status_code=status.HTTP_200_OK)
def get_message_with_chat_id(
    chat_id: int,
    current_user: User=Depends(get_current_user),
    db: Session=Depends(get_db)
):
    chat = db.get(Chat, chat_id)
    if not chat or chat.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return get_all_messages_with_chat_id(chat_id, db)