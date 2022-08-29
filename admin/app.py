from fastapi import FastAPI, Depends
from starlette.middleware.base import BaseHTTPMiddleware

from conf.config import get_app_settings
from .authen import authenticate
from .login import router as login_router
from .routes import router


class FastAPIAdmins(FastAPI):

    admin_path: str = get_app_settings().api_manager_prefix


admin_api = FastAPIAdmins(description="后台管理",
                          title="MyAdmin",
                          )


@router.get("/")
async def info(settings=Depends(get_app_settings)):
    return {
        "app_name": settings.title,
    }

admin_api.add_middleware(BaseHTTPMiddleware, dispatch=authenticate)
admin_api.include_router(router)
admin_api.include_router(login_router)

