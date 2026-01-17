from pydantic import BaseModel, Field
from typing import List

class ChatCreate(BaseModel):
    user_id:int
