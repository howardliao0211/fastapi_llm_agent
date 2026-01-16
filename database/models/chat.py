from database.models.base import BaseModel
from sqlmodel import Field, Relationship
from typing import List

class Chat(BaseModel, table=True):
    chat_id: int = Field(unique=True)
    history: List[str]
    user: "User" = Relationship(back_populates="chats")
