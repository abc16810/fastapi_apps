from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
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




# @app.get("/heroes/{hero_id}", response_model=HeroRead)
# def read_hero(hero_id: int):
#     with Session(engine) as session:
#         hero = session.get(Hero, hero_id)
#         if not hero:
#             raise HTTPException(status_code=404, detail="Hero not found")
#         return hero