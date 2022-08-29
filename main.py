import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from tortoise.contrib.fastapi import register_tortoise

from admin.app import admin_api
from apps import api
from apps.errors import (
    http_error_handler,
    http422_error_handler,
    server_error_exception,
    not_found_error_exception,
    forbidden_error_exception,
    unauthorized_error_exception,
)
from conf.config import get_app_settings
from conf.events import create_start_app_handler, create_stop_app_handler


def get_application() -> FastAPI:
    settings = get_app_settings()
    application = FastAPI(**settings.fastapi_kwargs)
    # 跨域
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_event_handler(
        "startup",
        create_start_app_handler(admin_api, settings),
    )

    application.add_event_handler(
        "shutdown",
        create_stop_app_handler(application),
    )

    # 数据库
    register_tortoise(application,
                      config={
                          "connections": {"default": {
                              'engine': 'tortoise.backends.mysql',
                              'credentials': {
                                  'host': settings.mysql_dict.mysql_host,
                                  'port': settings.mysql_dict.mysql_port,
                                  'user': settings.mysql_dict.mysql_user,
                                  'password': settings.mysql_dict.mysql_password,
                                  'database': settings.mysql_dict.mysql_db
                              }
                          }
                          },
                          "apps": {
                              "models": {
                                  "models": ["admin.models", "apps.models"],
                                  "default_connection": "default",
                              }
                          },
                      },
                      generate_schemas=True,
                      add_exception_handlers=True,
                      )

    application.mount(settings.api_manager_prefix, admin_api,)

    # errors
    application.add_exception_handler(HTTPException, http_error_handler)
    # 替换RequestValidationError 验证错误返回
    # @app.exception_handler(RequestValidationError)
    # async def validation_exception_handler(_: Request, exc: RequestValidationError):
    #    pass
    application.add_exception_handler(RequestValidationError, http422_error_handler)
    application.add_exception_handler(HTTP_500_INTERNAL_SERVER_ERROR, server_error_exception)
    application.add_exception_handler(HTTP_404_NOT_FOUND, not_found_error_exception)
    application.add_exception_handler(HTTP_403_FORBIDDEN, forbidden_error_exception)
    application.add_exception_handler(HTTP_401_UNAUTHORIZED, unauthorized_error_exception)

    # router
    application.include_router(api.router, prefix=settings.api_prefix)

    return application


app = get_application()

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8082, reload=True,
                log_config="logs.ini", debug=True)
