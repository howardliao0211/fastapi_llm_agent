from database.models.message import Message, Role
from pydantic import BaseModel, Field

class MessageCreate(BaseModel):
    role: Role = Field(...)
    content: str = Field(..., max_length=255)

class ResponseMessage(BaseModel):
    role: Role
    content: str
