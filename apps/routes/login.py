from fastapi import Body
from fastapi import APIRouter, Body, Depends, HTTPException
from conf.config import get_app_settings
from apps.models import User_Pydantic, UserTokenResponse, Users
from conf import constants
from apps.schemas import UserInCreate
from apps.jwt import create_access_token_for_user
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST


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


