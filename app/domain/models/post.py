from dataclasses import dataclass, field
from datetime import datetime

from app.domain.exceptions import InvalidFieldValue
from app.domain.models.base import BaseModel
from app.domain.models.user import User


@dataclass(kw_only=True)
class Post(BaseModel):
    post_id: int | None = None
    title: str
    created: datetime = field(default_factory=datetime.utcnow)
    updated: datetime = field(default_factory=datetime.utcnow)
    user: User | None = field(default=None)

    @staticmethod
    def validate_title(value: str) -> str:
        if len(value.strip()) == 0:
            raise InvalidFieldValue(field_name="title", field_value=value)
        return value.strip()
