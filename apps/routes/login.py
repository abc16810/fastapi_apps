from fastapi import Body
from fastapi import APIRouter, Body, Depends, HTTPException
from conf.config import get_app_settings
from apps.models import User_Pydantic, UserTokenResponse, Users, UserName
from conf import constants
from apps.schemas import UserInCreate, UserInLogin
from apps.jwt import create_access_token_for_user
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from .auth import get_current_user_authorizer
from tortoise.expressions import Q
from starlette.status import HTTP_201_CREATED
from fastapi.responses import RedirectResponse, JSONResponse
from utils import check_password
from typing import Optional


router = APIRouter()


@router.post("",
             response_model=UserTokenResponse,
             status_code=HTTP_201_CREATED,
             name="auth:register",
             summary="注册")
async def register(
        user: UserInCreate = Body(..., embed=True, alias="user"),
        settings=Depends(get_app_settings)
):
    """注册用户"""
    if await Users.get_or_none(username=user.username):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=constants.USERNAME_TAKEN,
        )
    if await Users.get_or_none(email=user.email):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=constants.EMAIL_TAKEN,
        )
    user_obj = await Users.create(**user.dict())
    token = create_access_token_for_user(
        user_obj,
        str(settings.secret_key.get_secret_value()),
    )
    return UserTokenResponse(
            username=user_obj.username,
            email=user_obj.email,
            avatar=user_obj.avatar,
            token=token,
        )


@router.post("/login", name="auth:login")
async def login(
    user_login: UserInLogin = Body(..., embed=True, alias="user"),
    settings=Depends(get_app_settings),
):
    wrong_login_error = HTTPException(
        status_code=HTTP_400_BAD_REQUEST,
        detail="incorrect email or password"
    )

    if '@' not in user_login.username_email:
        user = await Users.get_or_none(username=user_login.username_email)
    else:
        user = await Users.get_or_none(email=user_login.username_email)
    if not user:
        raise wrong_login_error

    if not check_password(user_login.password, user.password):
        raise wrong_login_error

    token = create_access_token_for_user(
        user,
        str(settings.secret_key.get_secret_value()),
    )
    # return UserTokenResponse(
    #     username=user.username,
    #     email=user.email,
    #     avatar=user.avatar,
    #     token=token,
    # )
    response = JSONResponse({"msg": "login success"},
                            status_code=HTTP_201_CREATED,
                            headers={"Authorization": "Token {}".format(token)}
                            )
    return response


@router.post("/test",status_code=HTTP_201_CREATED,
             name="aaa",
             summary="注册")
async def test(user: UserName = Body(..., embed=True, alias="user")):
    info = user.dict()
    info['password'] = "123456"
    try:
        await Users.create(**info)
    except Exception as err:
        raise HTTPException(detail="%s" % str(err), status_code=HTTP_500_INTERNAL_SERVER_ERROR)
    return user.dict()


# 必须验证
@router.get("/username")
async def test_auth(user: UserName = Depends(get_current_user_authorizer())):
    print(user.is_active)
    return user


# 有token时验证 没有时不验证
@router.get("/username2")
async def test_auth(user: Optional[UserName] = Depends(get_current_user_authorizer(required=False))):
    if user:
        return await UserName.from_tortoise_orm(user)
    return {"detail": "ok"}
