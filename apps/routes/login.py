from fastapi import Body
from fastapi import APIRouter
from apps.models import User_Pydantic, UserCreate_Pydantic, Users
from apps.schemas import UserInCreate

router = APIRouter()


@router.post("/users", response_model=User_Pydantic)
async def create_user(user: UserInCreate):
    print(user.dict())
    # user_obj = await Users.create(**user.dict(exclude_unset=True))
    # return await User_Pydantic.from_tortoise_orm(user_obj)
    return {}