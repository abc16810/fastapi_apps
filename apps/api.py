from fastapi import APIRouter
from apps.routes import info, login
from apps import signals


router = APIRouter()


router.include_router(info.router, tags=["info"], prefix="/info")
router.include_router(login.router, tags=["authentication"], prefix="/users")
