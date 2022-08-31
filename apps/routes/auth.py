from typing import Callable
from fastapi import Security, Depends, HTTPException
from starlette import status
from apps import jwt
from conf.config import get_app_settings
from fastapi.security.api_key import APIKeyHeader
from apps.models import UserName, Users
from typing import Optional


HEADER_KEY = "Authorization"
WRONG_TOKEN_PREFIX = "unsupported authorization type"


def get_current_user_authorizer(*, required: bool = True) -> Callable:  # type: ignore
    return _get_current_user if required else _get_current_user_optional


def _get_authorization_header_retriever(
    *,
    required: bool = True,
) -> Callable:  # type: ignore
    return _get_authorization_header if required else _get_authorization_header_optional


def _get_authorization_header(
    api_key: str = Security(APIKeyHeader(name=HEADER_KEY)),
    settings=Depends(get_app_settings),
) -> str:
    try:
        token_prefix, token = api_key.split(" ")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=WRONG_TOKEN_PREFIX,
        )
    if token_prefix != settings.jwt_token_prefix:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=WRONG_TOKEN_PREFIX,
        )
    return token


def _get_authorization_header_optional(
    authorization: Optional[str] = Security(
        APIKeyHeader(name=HEADER_KEY, auto_error=False),
    ),
    settings=Depends(get_app_settings),
) -> str:
    if authorization:
        return _get_authorization_header(authorization, settings)

    return ""


async def _get_current_user(
    token: str = Depends(_get_authorization_header_retriever()),
    settings=Depends(get_app_settings),
) -> UserName:
    try:
        username = jwt.get_username_from_token(
            token,
            str(settings.secret_key.get_secret_value()),
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="could not validate credentials"
        )

    user = await Users.get_or_none(username=username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="could not validate credentials",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="could not validate credentials",
        )
    return user


async def _get_current_user_optional(
    token: str = Depends(_get_authorization_header_retriever(required=False)),
    settings=Depends(get_app_settings),
) -> Optional[Users]:
    if token:
        return await _get_current_user(token, settings)

    return None
