from abc import ABC, abstractmethod
from typing import List

from app.domain.models.post import Post


class PostRepository(ABC):

    @abstractmethod
    async def create(self, post: Post) -> Post: ...

    @abstractmethod
    async def get_by_id(self, post_id: int) -> Post: ...

    @abstractmethod
    async def get_posts(self) -> List[Post]: ...

    @abstractmethod
    async def update(self, post: Post) -> Post: ...

    @abstractmethod
    async def delete(self, post_id: int) -> None: ...
