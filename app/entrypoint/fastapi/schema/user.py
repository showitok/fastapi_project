from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    user_id: int
    email: EmailStr
    created: datetime = Field(default_factory=datetime.utcnow)
