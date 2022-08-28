from fastapi import HTTPException
from fastapi.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED


def get_redis(request: Request):
    return request.app.redis


def get_current_admin(request: Request):
    admin = request.state.admin
    if not admin:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
    return admin
