import re
import uuid
from aioredis import Redis
from dataclasses import dataclass, field
from fastapi import APIRouter, Depends, Query, HTTPException, Body
from fastapi.logger import logger
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, Response, JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_303_SEE_OTHER
from typing import Dict
from tortoise import signals
from admin.models import Admin
from depends import get_redis
from utils import check_password, hash_password
from .constants import LOGIN_PATH, LOGIN_USER, LOGOUT_PATH
from .constants import access_token
from .templates import templates

router = APIRouter()


@dataclass
class DefaultDependency:
    kwargs: Dict = field(default_factory=dict, init=False)  # 其它参数 默认{}


@dataclass
class PostParams(DefaultDependency):
    """login parameters."""

    username: str = Body(
        ..., title="user", description="请输入用户名称"
    )
    password: str = Body(
        ..., title="passwd ", description="请输入密码", max_length=100, min_length=6
    )
    re: bool = Body(False, description='记住登录')

    def __post_init__(self):
        """post init"""
        self.kwargs['test'] = "aa"
        username = self.username
        passwd = self.password
        if not username or len(username) < 3 or len(username) >30:
            raise HTTPException(status_code=200,  detail="Invalid username")
        if not re.match('^[a-zA-Z]', username):
            raise HTTPException(status_code=200, detail="username must start with a letter")
        username = username.strip()
        if re.match('\w+', username).group() != username:
            raise HTTPException(status_code=200, detail="Invalid username")
        self.kwargs["username"] = username
        if not passwd or len(passwd) < 6:
            raise HTTPException(status_code=200, detail="Invalid password")
        self.kwargs['password'] = passwd


@router.post(LOGIN_PATH, summary="登录接口", description="提交用户名和密码")
async def login(request: Request, post_params=Depends(PostParams), redis: Redis = Depends(get_redis)):
    """
    描述信息
    """
    username = post_params.kwargs.get("username")
    password = post_params.kwargs.get("password")
    rember = post_params.re
    logger.info(password)
    logger.info(username)
    admin = await Admin.get_or_none(username=username)
    if not admin or not check_password(password, admin.password):
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="login_failed")

    response = RedirectResponse(url=request.app.admin_path, status_code=HTTP_303_SEE_OTHER)

    if rember:
        expire = 3600 * 24 * 30
        response.set_cookie("remember_me", "on")
    else:
        expire = 3600
        response.delete_cookie("remember_me")
    token = uuid.uuid4().hex
    response.set_cookie(
        access_token,
        token,
        expires=expire,
        path=request.app.admin_path,
        httponly=True,
    )
    await redis.set(LOGIN_USER.format(token=token), admin.pk, ex=expire)
    return response


@router.get(LOGOUT_PATH, summary="登出接口", description="登出")
async def logout(request: Request):
    # response =  RedirectResponse(
    #     url=request.app.admin_path, status_code=HTTP_303_SEE_OTHER
    # )
    response = JSONResponse(status_code=200, content={"detail": "logout success"})
    response.delete_cookie(access_token, path=request.app.admin_path)
    token = request.cookies.get(access_token)
    await request.app.redis.delete(LOGIN_USER.format(token=token))
    return response


def redirect_login(request: Request):
    return RedirectResponse(
        url=request.app.admin_path + LOGIN_PATH, status_code=HTTP_303_SEE_OTHER
    )


@router.get("/init", summary="初始化数据", description="初始化")
async def init_view(request: Request):
    exists = await Admin.all().limit(1).exists()
    if exists:
        return redirect_login(request)
    return templates.TemplateResponse("init.html", context={"request": request})


@router.post("/init", summary="初始化数据", description="初始化")
async def init(
    request: Request,
):
    exists = await Admin.all().limit(1).exists()
    if exists:
        return RedirectResponse(
                url=request.app.admin_path + LOGIN_PATH, status_code=HTTP_303_SEE_OTHER
            )
    form = await request.form()
    password = form.get("password")
    confirm_password = form.get("confirm_password")
    username = form.get("username")
    detail = "create success"
    if password != confirm_password:
        detail = "confirm_password_different"
    await Admin.create(username=username, password=password)
    return JSONResponse(status_code=201, content={"detail": detail})


async def pre_save_admin(_, instance: Admin, using_db, update_fields):
    if instance.pk:
        db_obj = await instance.get(pk=instance.pk)
        if db_obj.password != instance.password:
            instance.password = hash_password(instance.password)
    else:
        instance.password = hash_password(instance.password)

signals.pre_save(Admin)(pre_save_admin)
