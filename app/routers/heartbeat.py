from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/heartbeat",
    include_in_schema=False,
)


@router.get("/readiness", status_code=status.HTTP_200_OK)
def readiness() -> JSONResponse:
    return JSONResponse({"status": "readiness"})


@router.get("/liveness", status_code=status.HTTP_200_OK)
def liveness() -> JSONResponse:
    return JSONResponse({"status": "liveness"})
