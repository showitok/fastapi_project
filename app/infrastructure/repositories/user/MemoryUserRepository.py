from typing import Optional, Dict, Any
from app.domain.models.user import User
from app.domain.repositories.user import UserRepository
from app.infrastructure.persistences.memory_db.database import Database


class MemoryUserRepository(UserRepository):

    def __init__(self, database: Database):
        self._database = database

    async def get_by_id(self, user_id: int) -> Optional[User]:
        if not (user_data := self._database.users.get(user_id)):
            return None

        return self._build_user_model(user_data)

    @staticmethod
    def _build_user_model(user_data: Dict[str, Any]) -> User:
        return User(
            user_id=user_data.get('user_id'),
            email=user_data.get('email'),
            created=user_data.get('created'),
            updated=user_data.get('updated'),
        )
