from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Body
from typing import Union, List
from functools import lru_cache
from pathlib import Path
import aiofiles
from .handles import UploadFileParam
import os
from config import Settings

router = APIRouter(prefix="/api",
                   tags=["API"],                                  # 前端显示tag
                   # dependencies=[],                             # 当前全局依赖
                   responses={404: {"msg": "Not founds"}}  # 当请求不匹配（不存在）的uri时提示404
                   )
# 文件上传路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = Path(BASE_DIR, "./uploads")


@lru_cache()
def get_settings():
    return Settings()


@router.get("/info")
async def info(settings: Settings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
        "author": settings.author,
        "development_time": settings.development_time,
    }


@router.post("/files/", summary='test')
async def create_file(files: List[bytes] = File()):
    return {"file_sizes": [len(file) for file in files]}


@router.post("/uploadfile/")
async def create_upload_file(params=Depends(UploadFileParam)):
    """
    文件上传
    """
    file = params.file
    identifier = params.identifier
    num = params.number
    path = os.path.join(UPLOAD_DIR, identifier)
    prefix = params.kwargs['prefix']
    if not os.path.exists(path):
        os.makedirs(path)
    file_name = Path(path, f'{identifier}_{num}.{prefix}')
    if not os.path.exists(file_name):
        async with aiofiles.open(file_name, 'wb') as f:
            await f.write(await file.read())
    return {
        'code': 1,
        'chunk': f'{identifier}_{num}.{prefix}'
            }



