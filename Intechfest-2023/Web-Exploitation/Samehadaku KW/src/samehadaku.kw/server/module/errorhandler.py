from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import JSONResponse
from fastapi import (
    FastAPI,
    Request,
)
from zipfile import BadZipFile


def add_error_handler(app: FastAPI):
    @app.exception_handler(AuthJWTException)
    async def _(_: Request, exc: AuthJWTException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message}
        )

    @app.exception_handler(BadZipFile)
    async def _(_: Request, exc: BadZipFile):
        return JSONResponse(
            status_code=400,
            content={"message": str(exc)}
        )
