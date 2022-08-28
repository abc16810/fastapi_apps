import uvicorn
from aioredis import from_url
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.exceptions import StarletteHTTPException, RequestValidationError
from fastapi.logger import logger
from fastapi.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from tortoise.contrib.fastapi import register_tortoise

from admin.app import admin_api
from apps import info
from config import Settings


description = """练习测试。。。 🚀"""
s = Settings()

if s.redis_passwd and not s.redis_user:
    redis_url = f'redis://:{s.redis_passwd}@{s.redis_host}/{s.redis_db}'


app = FastAPI(description=description,
              title="MyApp",
              version="0.0.1",
              terms_of_service="http://example.com/terms/",
              openapi_url="/api/v1/openapi.json",
              responses={404: {"msg": "Not founds"}}  # 当请求不匹配（不存在）的uri时提示404
              )

# 跨域请求
origins = [
    "http://localhost:8088",
    "http://127.0.0.1:8088"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 替换HTTPException默认返回
# async def server_error_exception(request: Request, exc: HTTPException):
#     logger.info(exc)
#     logger.info("%s: the request is : %s " % (HTTP_500_INTERNAL_SERVER_ERROR, request))
# #

async def server_error_exception(request: Request, exc: HTTPException):
    return JSONResponse(content={"detail": "Server Error"}, status_code=200)


async def not_found_error_exception(request: Request, exc: HTTPException):
    return JSONResponse(content={"detail": "Oops… You just found an error page"}, status_code=exc.status_code)


async def forbidden_error_exception(request: Request, exc: HTTPException):
    return JSONResponse(content={"detail": "Oops… You are forbidden"}, status_code=exc.status_code)


async def unauthorized_error_exception(request: Request, exc: HTTPException):
    return JSONResponse(content={"detail": "Oops… You are unauthorized"}, status_code=exc.status_code)

app.add_exception_handler(HTTP_500_INTERNAL_SERVER_ERROR, server_error_exception)
app.add_exception_handler(HTTP_404_NOT_FOUND, not_found_error_exception)
app.add_exception_handler(HTTP_403_FORBIDDEN, forbidden_error_exception)
app.add_exception_handler(HTTP_401_UNAUTHORIZED, unauthorized_error_exception)


@app.on_event("startup")
async def startup():
    r = from_url(
        redis_url,
        decode_responses=True,
        encoding="utf8",
    )
    await admin_api.configure(
        redis=r
    )

# 连接库
register_tortoise(
    app,
    config={
        "connections": {"default": {
            'engine': 'tortoise.backends.mysql',
            'credentials': {
                'host': s.mysql_host,
                'port': s.mysql_port,
                'user': s.mysql_user,
                'password': s.mysql_passwd,
                'database': s.mysql_table
            }
        }
        },
        "apps": {
            "models": {
                "models": ["admin.models"],
                "default_connection": "default",
            }
        },
    },
    generate_schemas=True,
)

app.mount('/admin', admin_api)
app.include_router(info.router)


if __name__ == "__main__":

    if s.debug:
        uvicorn.run(app="main:app", host="127.0.0.1", port=8088, reload=True,
                    log_config="logs.ini",
                    debug=True)
    else:
        uvicorn.run(app="main:app", host="0.0.0.0", port=8088)
