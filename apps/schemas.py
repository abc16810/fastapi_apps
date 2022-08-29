from pydantic import BaseModel, EmailStr, validator
from typing import Union
from datetime import datetime
import re


def validator_username_email(value: Union[EmailStr, str]) -> Union[EmailStr, str]:
    if isinstance(value, str):
        if not value or len(value) < 3 or len(value) >30:
            raise ValueError("Name length must be > 3")
        if not re.match('^[a-zA-Z]', value):
            raise ValueError("username must start with a letter")
            value = value.strip()
        if re.match('\w+', value).group() != value:
            raise ValueError("Invalid username")
        return value
    return value


class UserInLogin(BaseModel):
    username_email: Union[EmailStr, str]
    password: str
    _normalize_name = validator('username_email', allow_reuse=True)(validator_username_email)


class UserInCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

    # validators
    _normalize_name = validator('username', allow_reuse=True)(validator_username_email)

    @validator("password")
    def validator_name(cls, v):
        if v and len(v) < 6:
            raise ValueError("password length must be > 6")
        return v


# JWT
class JWTModel(BaseModel):
    exp: datetime
    sub: str


class JWTUser(BaseModel):
    username: str



