from fastapi import APIRouter
from apps.routes import info, login, security, security2
from apps import signals


router = APIRouter()


router.include_router(info.router, tags=["info"], prefix="/info")
router.include_router(login.router, tags=["authentication"], prefix="/users")
router.include_router(security.router, tags=["security"], prefix="/security")
router.include_router(security2.router, tags=["security2"], prefix="/security2")