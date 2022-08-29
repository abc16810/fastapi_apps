from fastapi.requests import Request
from starlette.middleware.base import RequestResponseEndpoint
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from aioredis import Redis
from .constants import access_token, LOGIN_USER, LOGIN_PATH
from admin.models import Admin
from fastapi.logger import logger


async def authenticate(
        request: Request,
        call_next: RequestResponseEndpoint,
):
    redis = request.app.state.redis  # type:Redis
    token = request.cookies.get(access_token)
    path = request.scope["path"]
    admin = None
    if token:
        token_key = LOGIN_USER.format(token=token)
        admin_id = await redis.get(token_key)
        admin = await Admin.get_or_none(pk=admin_id)
    request.state.admin = admin
    if path == LOGIN_PATH and admin:
        return RedirectResponse(url=request.app.admin_path, status_code=HTTP_303_SEE_OTHER)

    response = await call_next(request)
    return response
