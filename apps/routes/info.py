import aiofiles
import os
from fastapi import APIRouter, Depends, File
from pathlib import Path
from typing import List

from apps.handles import UploadFileParam, User, UPLOAD_DIR
from conf.config import get_app_settings

router = APIRouter()


@router.get("/info")
async def info(settings = Depends(get_app_settings)):
    return {
        "app_name": settings.title,
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


@router.post("/user")
async  def get_user(item: User):
    return item





