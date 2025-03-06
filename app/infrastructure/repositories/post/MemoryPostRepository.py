from typing import List, Dict, Any, Optional
from app.domain.models.post import Post
from app.domain.models.user import User
from app.domain.repositories import PostRepository
from app.infrastructure.persistences.memory_db.database import Database


class MemoryPostRepository(PostRepository):

    def __init__(self, database: Database):
        self.database = database

    async def create(self, post: Post) -> Post:
        post_data = self._serialize(post)
        self.database.posts[post_data["post_id"]] = post_data
        post.post_id = post_data["post_id"]
        return post

    async def get_by_id(self, post_id: int) -> Optional[Post]:
        if not (post_data := self.database.posts.get(post_id)):
            return None

        return self._build_post_model(post_data)

    async def get_posts(self) -> List[Post]:
        return [self._build_post_model(post_data) for post_data in self.database.posts.values()]

    async def update(self, post: Post) -> Post:
        if not post.modified_fields:
            return post

        self.database.posts[post.post_id].update(self._serialize(post, True))
        return post

    async def delete(self, post_id: int) -> None:
        if post_id in self.database.posts:
            self.database.posts.pop(post_id)

        return None

    def _serialize(self, post: Post, partial: bool = False) -> Dict[str, Any]:
        if not partial:
            return {
                "post_id": post.post_id or self._generate_id(),
                "title": post.title,
                "created": post.created,
                "updated": post.updated,
                "user_id": post.user.user_id
            }
        else:
            data = {}
            modified_fields = post.modified_fields
            for field in modified_fields:
                match field:
                    case "title":
                        data["title"] = post.title
                    case _:
                        pass
            return data

    def _generate_id(self) -> int:
        return len(self.database.posts) + 1

    @staticmethod
    def _build_post_model(post_data: Dict[str, Any]) -> Post:
        return Post(
            post_id=post_data["post_id"],
            title=post_data["title"],
            created=post_data["created"],
            updated=post_data["updated"],
            user=User(user_id=post_data["user_id"]),
        )
