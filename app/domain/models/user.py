import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from app.domain.exceptions import InvalidFieldValue
from app.domain.models.base import BaseModel

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')


@dataclass(kw_only=True)
class User(BaseModel):
    user_id: int
    email: Optional[str] = None
    created: datetime = field(default_factory=datetime.utcnow)
    updated: datetime = field(default_factory=datetime.utcnow)

    @staticmethod
    def validate_email(email: Optional[str]) -> Optional[str]:
        if (email is not None) and not EMAIL_REGEX.match(email):
            raise InvalidFieldValue(field_name="email", field_value=email)
        return email
