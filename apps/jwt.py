from jose import JWTError, jwt
from typing import Dict, Union
from apps.models import Users
from pydantic import ValidationError
from datetime import datetime, timedelta
from apps.schemas import JWTModel, JWTUser
from fastapi.security import APIKeyHeader

JWT_SUBJECT = "access"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24  # one day


def create_jwt_token(
    *,
    jwt_content: Dict[str, str],
    secret_key: str,
    expires_delta: Union[timedelta, None] = None
) -> str:
    to_encode = jwt_content.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update(JWTModel(exp=expire, sub=JWT_SUBJECT).dict())
    return jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)


def create_access_token_for_user(user: Users, secret_key: str) -> str:
    return create_jwt_token(
        jwt_content=JWTUser(username=user.username).dict(),
        secret_key=secret_key,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )


def get_username_from_token(token: str, secret_key: str) -> str:
    try:
        res = JWTUser(**jwt.decode(token, secret_key, algorithms=[ALGORITHM]))
        print(res)
        return res.username
    except JWTError as decode_error:
        raise ValueError("unable to decode JWT token") from decode_error
    except ValidationError as validation_error:
        raise ValueError("malformed payload in token") from validation_error




