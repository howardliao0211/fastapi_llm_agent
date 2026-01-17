from database.models.base import BaseModel
from sqlmodel import Field, Relationship
from typing import List

class User(BaseModel, table=True):

    # Setting index=True allow SQL to query these properties faster.
    # ex: select(User).where(username="Howard")
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    full_name: str
    password: str

    chats: List["Chat"] = Relationship(back_populates="user")
