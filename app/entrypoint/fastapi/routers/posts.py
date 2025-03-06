from typing import List

from fastapi import APIRouter, status

from app.entrypoint.fastapi.schema.post import Post, PostCreateInput, PostUpdateInput
from app.entrypoint.fastapi.schema.user import User
from app.application.dic import DIC
from app.domain.models.post import Post as PostModel
from app.domain.models.user import User as UserModel

__all__ = ("router", )


router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


@router.get(
    "",
    response_model=List[Post],
    description="Get all posts",
    status_code=status.HTTP_200_OK
)
async def list_posts() -> List[Post]:
    posts: List[PostModel] = await DIC.post_service.list_posts()
    return [to_post_view_model(post) for post in posts]


@router.get(
    "/{post_id}",
    response_model=Post,
    description="Get posts",
    status_code=status.HTTP_200_OK
)
async def get_post(post_id: int) -> Post:
    post: PostModel = await DIC.post_service.get_post(post_id)
    return to_post_view_model(post)


@router.post(
    "",
    response_model=Post,
    description="Create a new post",
    status_code=status.HTTP_201_CREATED
)
async def create_post(input_post: PostCreateInput) -> Post:
    post: PostModel = await DIC.post_service.create_post(input_post.user_id, input_post.title)
    return to_post_view_model(post)


@router.patch(
    "/{post_id}",
    response_model=Post,
    description="Update a  post",
    status_code=status.HTTP_200_OK
)
async def update_post(post_id: int, input_post: PostUpdateInput) -> Post:
    post: PostModel = await DIC.post_service.update_post(input_post.user_id, post_id, input_post.title)
    return to_post_view_model(post)


@router.delete(
    "/{post_id}",
    description="Delete a  post",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_post(post_id: int) -> None:
    await DIC.post_service.delete_post(post_id)


def to_post_view_model(post: PostModel) -> Post:
    return Post(
        post_id=post.post_id,
        title=post.title,
        created=post.created,
        user=to_user_view_model(post.user),
    )


def to_user_view_model(user: UserModel) -> User:
    return User(
        user_id=user.user_id,
        email=user.email,
        created=user.created,
    )
