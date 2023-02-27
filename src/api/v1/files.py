import os
import shutil
from typing import Any, AnyStr, Dict, List

from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse

from src.api.v1.users import verify_token
from src.core.config import app_settings
from src.db.db import get_session
from src.schemas.files import FileCreate, FileInDBBase
from src.services.base import file_crud

router = APIRouter()


@router.post('/upload', response_model=Dict, status_code=status.HTTP_201_CREATED)
async def upload(
    db: AsyncSession = Depends(get_session), file: UploadFile = File(), user: bool = Depends(verify_token)
) -> Any:
    """
    Upload file.
    """
    name = file.filename
    _path = os.path.join(app_settings.DEFAULT_FILES_FOLDER, name)

    if not os.path.isdir(app_settings.DEFAULT_FILES_FOLDER):
        os.mkdir(app_settings.DEFAULT_FILES_FOLDER)

    with open(_path, 'wb') as f:
        shutil.copyfileobj(file.file, f)

    obj_in = FileCreate(path=_path, name=name, size=file.size, owner=user.id)
    exists = await file_crud.get(db=db, name=name)

    if exists:
        await file_crud.delete(db=db, name=name)

    new_file = await file_crud.create(db=db, obj_in=obj_in)
    response = {
        "id": new_file.id,
        "name": new_file.name,
        "created_at": new_file.created_at,
        "path": new_file.path,
        "size": new_file.size,
        "is_downloadable": new_file.is_downloadable
    }
    return response


@router.get('/download', response_model=FileInDBBase | AnyStr, status_code=status.HTTP_200_OK)
async def download(path: str = '', is_archive: bool = False, user: bool = Depends(verify_token)) -> Any:
    """
    Download file.
    """
    path_split = path.split('/')
    filename = path_split[-1]
    head_dir = path_split[0]
    last_dir = path_split[-2]
    path_dir = str()

    for _dir in path_split[:-1]:
        path_dir += _dir

    dir_items = os.listdir(head_dir)

    for item in dir_items:  # clear .zip folders
        if item.endswith(app_settings.DOT + app_settings.ZIP_FORMAT):
            os.remove(os.path.join(head_dir, item))

    if not os.path.isfile(path):
        return app_settings.FILE_NOT_EXIST

    if is_archive:
        archive = shutil.make_archive(last_dir, app_settings.ZIP_FORMAT, path_dir)
        response = FileResponse(
            path=archive, media_type=app_settings.TYPE_OCTET_STREAM, filename=last_dir + app_settings.DOT
            + app_settings.ZIP_FORMAT
        )
    else:
        response = FileResponse(path, media_type=app_settings.TYPE_OCTET_STREAM, filename=filename)

    return response


@router.get('/', response_model=List, status_code=status.HTTP_200_OK)
async def info(
    db: AsyncSession = Depends(get_session), skip: int = 0, limit: int = 100, user: bool = Depends(verify_token)
) -> Any:
    """
    Retrieve files info.
    """
    response = await file_crud.get_multi(db=db, skip=skip, limit=limit)
    return response
