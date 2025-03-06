from datetime import datetime

from pydantic import BaseModel, Field

from app.entrypoint.fastapi.schema.user import User


class Post(BaseModel):
    post_id: int
    title: str
    created: datetime = Field(default_factory=datetime.utcnow)
    user: User


class PostCreateInput(BaseModel):
    title: str
    user_id: int


class PostUpdateInput(BaseModel):
    title: str
    user_id: int
