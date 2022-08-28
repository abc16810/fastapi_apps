from aioredis import Redis
from fastapi import FastAPI, Depends
from starlette.middleware.base import BaseHTTPMiddleware

from config import Settings
from utils import get_settings
from .authen import authenticate
from .login import router as login_router
from .routes import router


class FastAPIAdmins(FastAPI):

    admin_path: str
    redis: Redis

    async def configure(
            self,
            redis: Redis,
            admin_path: str = "/admin",
    ):
        self.redis = redis
        self.admin_path = admin_path


admin_api = FastAPIAdmins(description="后台管理",
                          title="MyAdmin",
                          responses={404: {"msg": "Not founds"}}
                          )


@router.get("/")
async def info(settings: Settings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
    }


admin_api.add_middleware(BaseHTTPMiddleware, dispatch=authenticate)
admin_api.include_router(router)
admin_api.include_router(login_router)

