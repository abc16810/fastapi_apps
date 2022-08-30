from datetime import datetime
from pydantic import EmailStr, validator
from sqlmodel import Field, SQLModel, Relationship, func
from typing import List
from typing import Optional


class Users(SQLModel, table=True):
    __tablename__ = "users_test"


    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, max_length=30, index=True)
    email:EmailStr = Field(default=None, unique=True)
    password: str
    last_login: datetime = Field(description="Last Login", default=datetime.now())
    avatar: str  = Field(max_length=200, default="")
    is_active: bool = True
    is_superuser: bool = False

    def __str__(self) -> str:
        return "%s" % self.username


# 只是 Pydantic 模型
class UserCreate(SQLModel):
    username: str
    email: EmailStr
    password: str

    @validator("password")
    def validator_password(cls, v):
        if v and len(v) < 6:
            raise ValueError("password length must be > 6")
        return v


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    heroes: List["Hero"] = Relationship(back_populates="team")


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)

    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    team: Optional[Team] = Relationship(back_populates="heroes")


