from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from .auth import get_current_user_authorizer
from sqlmodel import Session
from apps.db import *


router = APIRouter()


@router.get("/create")
async def create():
    """创建数据库表"""
    create_db_and_tables()


@router.post("/users/", summary="创建用户")
async def create_hero(user: UserCreate, session: Session = Depends(get_session)):
    # .from_orm() 方法从另一个具有属性的对象中读取数据并创建该类的新实例
    try:
        db_user = Users.from_orm(user) # from_orm() 创建一个新的 Users（这是将数据保存到数据库的实际表模型)
        session.add(db_user)
        await session.commit()
    except Exception as err:
        print(err)
    return JSONResponse({"detail": "success"}, status_code=200)


@router.get("/users/{user_id}", response_model=UserRead)
async def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(Users, user_id)  # one
    if not user:
        raise HTTPException(status_code=404, detail="Hero not found")
    return user


@router.patch("/users/{user_id}", response_model=UserRead)
async def update_user(
user_id: int,
u: UserUpdate,
    session: Session = Depends(get_session)

):
    db_user = session.get(Users, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Team not found")
    user_data = u.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    try:
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user
    except Exception as err:
        print(err)


@router.delete("/users/{user_id}")
def delete_team(*, session: Session = Depends(get_session), user_id: int):
    user = session.get(Users, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Team not found")
    session.delete(user)
    session.commit()
    return {"ok": True}
