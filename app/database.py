import random
from datetime import datetime
from dataclasses import dataclass, field

__all__ = ("database", )


@dataclass
class Database:
    posts: dict = field(default_factory=dict)
    users: dict = field(default_factory=dict)

    def __post_init__(self):
        # noinspection PyTypeChecker
        self.users = {
            user_id: {
                "user_id": user_id,
                "email": f"user_{user_id}@example.com",
                "created": datetime.utcnow(),
            }
            for user_id in range(1, 4)
        }

        # noinspection PyTypeChecker
        self.posts = {
            post_id: {
                "post_id": post_id,
                "title": f"FastAPI tutorial {post_id}",
                "created": datetime.utcnow(),
                "user_id": random.choice(list(self.users.keys()))
            }
            for post_id in range(1, 6)
        }


database = Database()
