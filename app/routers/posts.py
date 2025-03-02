from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/posts",
)


@router.get("", status_code=status.HTTP_200_OK)
async def get_posts() -> JSONResponse:
    return JSONResponse(
        [
            {"title": "FastAPI tutorial."},
            {"title": "Run fastAPI in docker."},
        ]
    )
