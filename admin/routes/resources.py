from fastapi import APIRouter, Depends
from config import Settings
from utils import get_settings


router = APIRouter()



@router.get("/info")
async def info(settings: Settings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
        "author": settings.author,
        "development_time": settings.development_time,
    }
