from pydantic import BaseModel, Field
from typing import List

def ChatCreate(BaseModel):
    history = Field(default_factory=list)

def ShowChat(BaseModel):
    id: int
    history: List[str]
