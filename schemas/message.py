from database.models.message import Message, Role
from pydantic import BaseModel, Field

class MessageCreate(BaseModel):
    role: Role = Field(default=Role.USER)
    content: str = Field(...)

class ShowMessage(BaseModel):
    id: int
    role: Role
    content: str
