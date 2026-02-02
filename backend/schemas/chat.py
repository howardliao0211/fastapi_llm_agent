from pydantic import BaseModel, Field, field_validator, EmailStr, ConfigDict

class ShowChat(BaseModel):
    id: int
    title: str
