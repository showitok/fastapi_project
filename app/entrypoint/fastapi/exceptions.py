from typing import Type
from fastapi import FastAPI, status
from fastapi.responses import ORJSONResponse

from app.domain import exceptions as domain_exceptions

DomainExceptionType = Type[domain_exceptions.DomainException]

EXCEPTION_STATUS_MAPPING: dict[DomainExceptionType, int] = {
    domain_exceptions.UserNotFound: status.HTTP_404_NOT_FOUND,
    domain_exceptions.PostNotFound: status.HTTP_404_NOT_FOUND,
    domain_exceptions.InvalidFieldValue: status.HTTP_400_BAD_REQUEST,
    domain_exceptions.Forbidden: status.HTTP_403_FORBIDDEN,
}


def setup_exceptions_handler(app: FastAPI) -> None:
    @app.exception_handler(domain_exceptions.DomainException)
    def domain_exception_handler(_, exc: domain_exceptions.DomainException) -> ORJSONResponse:
        return ORJSONResponse(
            content={
                "error": exc.message,
                "type": exc.TYPE
            },
            status_code = EXCEPTION_STATUS_MAPPING.get(exc.TYPE, status.HTTP_500_INTERNAL_SERVER_ERROR)
        )

    @app.exception_handler(Exception)
    def exception_handler(_, exc: Exception) -> ORJSONResponse:
        return ORJSONResponse(
            content={
                "error": str(exc),
                "type": "internal_server_error"
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
