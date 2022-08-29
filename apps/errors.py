from fastapi.exceptions import HTTPException, RequestValidationError, ValidationError
from fastapi.requests import Request
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from fastapi.responses import JSONResponse
from fastapi.logger import logger
from typing import Union


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse({"errors": [exc.detail]}, status_code=exc.status_code)


async def server_error_exception(_: Request, exc: HTTPException) -> JSONResponse:
    logger.info("error: %s" % exc.detail)
    return JSONResponse(content={"detail": "Server Error"}, status_code=exc.status_code)


async def not_found_error_exception(request: Request, exc: HTTPException) -> JSONResponse:
    logger.info("request: %s error: %s" % (request.scope['path'], exc.detail))
    return JSONResponse(content={"detail": "Oops… You just found an error page"}, status_code=exc.status_code)


async def forbidden_error_exception(_: Request, exc: HTTPException) -> JSONResponse:
    logger.info("error: %s" % exc.detail)
    return JSONResponse(content={"detail": "Oops… You are forbidden"}, status_code=exc.status_code)


async def unauthorized_error_exception(_: Request, exc: HTTPException) -> JSONResponse:
    logger.info("error: %s" % exc.detail)
    return JSONResponse(content={"detail": "Oops… You are unauthorized"}, status_code=exc.status_code)


async def http422_error_handler(
    _: Request,
    exc: Union[RequestValidationError, ValidationError],
) -> JSONResponse:
    return JSONResponse(
        {"errors": exc.errors()},
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
    )