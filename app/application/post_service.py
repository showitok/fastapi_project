from typing import List
from app.domain.exceptions import UserNotFound, PostNotFound, Forbidden
from app.domain.models.post import Post
from app.domain.repositories import PostRepository, UserRepository


class PostService:

    def __init__(self, post_repository: PostRepository, user_repository: UserRepository):
        self.post_repository = post_repository
        self.user_repository = user_repository

    async def create_post(self, user_id: int, title: str) -> Post:
        if not (user := await self.user_repository.get_by_id(user_id)):
            raise UserNotFound(user_id=user_id)
        post = Post(title=title, user=user)
        return await self.post_repository.create(post)

    async def get_post(self, post_id: int) -> Post:
        if not (post := await self.post_repository.get_by_id(post_id)):
            raise PostNotFound(post_id=post_id)

        if not (user := await self.user_repository.get_by_id(post.user.user_id)):
            raise UserNotFound(user_id=post.user.user_id)

        post.user = user
        return post

    async def list_posts(self) -> List[Post]:
        posts = await self.post_repository.get_posts()
        for post in posts:
            post.user = await self.user_repository.get_by_id(post.user.user_id)

        return posts

    async def update_post(self, user_id: int, post_id: int, title: str) -> Post:
        if not (post := await self.post_repository.get_by_id(post_id)):
            raise PostNotFound(post_id=post_id)

        if post.user.user_id != user_id:
            raise Forbidden()

        if not (user := await self.user_repository.get_by_id(post.user.user_id)):
            raise UserNotFound(user_id=user_id)

        post.title = title
        post = await self.post_repository.update(post)
        post.user = user
        return post

    async def delete_post(self, post_id: int) -> None:
        await self.post_repository.delete(post_id)
