from dataclasses import dataclass
from typing import Optional

from app.application.post_service import PostService
from app.infrastructure.persistences.mysql.database import Database

__all__ = ("DIC", )


@dataclass(kw_only=True)
class DependencyInjectionContainer:
    post_service: Optional[PostService] = None
    mysql_database: Optional[Database] = None


DIC = DependencyInjectionContainer()
