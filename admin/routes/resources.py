from fastapi import APIRouter, Depends
from conf.config import get_app_settings


router = APIRouter()



@router.get("/info")
async def info(settings = Depends(get_app_settings)):
    return {
        "app_name": settings.app_name,
        "author": settings.author,
        "development_time": settings.development_time,
    }
