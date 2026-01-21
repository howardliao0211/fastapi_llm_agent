from fastapi import APIRouter, status, Depends
from schemas.message import MessageCreate, ResponseMessage
from schemas.chat import ShowChat
from database.crud.chat import insert_chat
from database.crud.message import insert_message, handle_llm_turn
from database.models.user import User
from database.models.message import Role, Message
from database.models.chat import Chat
from sqlmodel import Session, select
from apis.deps import get_db, get_current_user
from services.llm_service import llm_service
from fastapi import HTTPException

router = APIRouter()

@router.post("/chats", response_model=ShowChat, status_code=201)
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

@router.post("/chats/{chat_id}/messages", response_model=ResponseMessage, status_code=201)
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
