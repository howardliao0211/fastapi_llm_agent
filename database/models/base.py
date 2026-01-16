from datetime import datetime
from sqlmodel import SQLModel, Field

class BaseModel(SQLModel):
    # id is None before inserting into the database. 
    # Hence, the default value is None.
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
