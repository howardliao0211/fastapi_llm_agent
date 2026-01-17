from database.models.base import BaseModel
from sqlmodel import Field, Relationship
from typing import List

class Chat(BaseModel, table=True):
    user_id: int = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="chats")
    messages: List["Message"] = Relationship(back_populates="chat")
