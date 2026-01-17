from database.models.base import BaseModel
from sqlmodel import Field, Relationship
from enum import Enum

class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"

class Message(BaseModel, table=True):
    chat_id: int = Field(foreign_key="chat.id")
    role: Role
    content: str

    chat: "Chat" = Relationship(back_populates="messages")

