from types import NoneType
from typing import List

from fastapi import APIRouter, status, HTTPException
from app.schema.post import Post, PostCreateInput, PostUpdateInput
from app.schema.user import User
from app.database import database

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
async def list_posts() -> List[Post] :
    return [
        Post(
            post_id=post["post_id"],
            title=post["title"],
            created=post["created"],
            user=User(
                user_id=post["user_id"],
                email=database.users[post["user_id"]]["email"],
                created=database.users[post["user_id"]]["created"],
            )
        )
        for post in database.posts.values()
    ]


@router.get(
    "/{post_id}",
    response_model=Post,
    description="Get posts",
    status_code=status.HTTP_200_OK
)
async def get_post(post_id: int) -> Post:
    if post_id not in database.posts:
        raise HTTPException(
            detail="Post not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

    post = database.posts[post_id]

    return Post(
        post_id=post["post_id"],
        title=post["title"],
        created=post["created"],
        user=User(
            user_id=post["user_id"],
            email=database.users[post["user_id"]]["email"],
            created=database.users[post["user_id"]]["created"],
        )
    )


@router.post(
    "",
    response_model=Post,
    description="Create a new post",
    status_code=status.HTTP_201_CREATED
)
async def create_post(input_post: PostCreateInput) -> Post:
    if input_post.user_id not in database.users:
        raise HTTPException(
            detail="User not found",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    post = Post(
        post_id=len(database.posts) + 1,
        title=input_post.title,
        user=User(
            user_id=input_post.user_id,
            email=database.users[input_post.user_id]["email"],
            created=database.users[input_post.user_id]["created"],
        )
    )

    database.posts[post.post_id] = {
        "post_id": post.post_id,
        "title": post.title,
        "created": post.created,
        "user_id": input_post.user_id,
    }

    return post


@router.patch(
    "/{post_id}",
    response_model=Post,
    description="Update a  post",
    status_code=status.HTTP_200_OK
)
async def update_post(post_id: int, input_post: PostUpdateInput) -> Post:
    if post_id not in database.posts:
        raise HTTPException(
            detail="Post not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

    post = database.posts[post_id]
    post["title"] = input_post.title

    return Post(
        post_id=post["post_id"],
        title=post["title"],
        created=post["created"],
        user=User(
            user_id=post["user_id"],
            email=database.users[post["user_id"]]["email"],
            created=database.users[post["user_id"]]["created"],
        )
    )


@router.delete(
    "/{post_id}",
    description="Delete a  post",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_post(post_id: int) -> None:
    if post_id not in database.posts:
        return

    database.posts.pop(post_id)
    return None
