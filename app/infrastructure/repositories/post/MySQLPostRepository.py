import logging
from typing import List, Dict, Any, Optional
from app.domain.models.post import Post
from app.domain.models.user import User
from app.domain.repositories import PostRepository
from app.infrastructure.persistences.mysql.database import Database


class MySQLPostRepository(PostRepository):

    def __init__(self, database: Database):
        self.connection_pool = database.pool

    async def create(self, post: Post) -> Post:
        async with self.connection_pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    query="INSERT INTO posts (post_id, title, created, updated, user_id) VALUES (%s, %s, %s, %s, %s)",
                    args=(
                        post.post_id,
                        post.title,
                        post.created,
                        post.updated,
                        post.user.user_id
                    )
                )
                post.post_id = cursor.lastrowid
        return post

    async def get_by_id(self, post_id: int) -> Optional[Post]:
        async with self.connection_pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    query="SELECT post_id, title, created, updated, user_id FROM posts WHERE post_id = %s",
                    args=(post_id,)
                )
                post_data = await cursor.fetchone()

        return self._build_post_model(post_data) if post_data else None

    async def get_posts(self) -> List[Post]:
        async with self.connection_pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    query="SELECT post_id, title, created, updated, user_id FROM posts",
                )
                posts = await cursor.fetchall()
        # logger.info("All posts: ", posts)
        return [self._build_post_model(post_data) for post_data in posts]

    async def update(self, post: Post) -> Post:
        if not (modified_data := self._serialize(post, True)):
            return post

        async with self.connection_pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    query=f"UPDATE posts SET {', '.join([f'`{key}` = %s' for key in modified_data.keys()])}",
                    args=tuple(modified_data)
                )

        return post

    async def delete(self, post_id: int) -> None:
        async with self.connection_pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    query=f"DELETE FROM posts WHERE post_id = %s",
                    args=(post_id,)
                )
        return None

    @staticmethod
    def _serialize(post: Post, partial: bool = False) -> Dict[str, Any]:
        if not partial:
            return {
                "post_id": post.post_id,
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

    @staticmethod
    def _build_post_model(post_data: Dict[str, Any]) -> Post:
        return Post(
            post_id=post_data["post_id"],
            title=post_data["title"],
            created=post_data["created"],
            updated=post_data["updated"],
            user=User(user_id=post_data["user_id"]),
        )
