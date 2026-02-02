from pydantic import BaseModel, Field, field_validator, EmailStr, ConfigDict

class UserCreate(BaseModel):
    # ... means the field is required and not optional with default=None
    full_name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr = Field(..., min_length=5, max_length=255)
    password: str = Field(..., min_length=4, max_length=50)

class ShowUser(BaseModel):
    id: int
    full_name: str
    email: EmailStr
