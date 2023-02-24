import os
import shutil

from typing import Any, AnyStr, Dict, List

from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.users import verify_token
from src.core.config import app_settings
from src.db.db import get_session
from src.services.base import file_crud
from src.schemas.files import FileCreate, FileInDBBase

router = APIRouter()


@router.post('/upload', response_model=FileInDBBase, status_code=status.HTTP_201_CREATED)
async def upload(
    db: AsyncSession = Depends(get_session), file: UploadFile = File(),  # user: bool = Depends(verify_token)
) -> Any:
    name = file.filename
    path = os.path.join(app_settings.DEFAULT_FILES_FOLDER, name)

    if not os.path.isdir(app_settings.DEFAULT_FILES_FOLDER):
        os.mkdir(app_settings.DEFAULT_FILES_FOLDER)

    with open(path, 'wb') as f:
        shutil.copyfileobj(file.file, f)
    #  Не считает размер файла
    size = int(round(os.path.getsize(path) / 1048576, 0))  # per Mb
    # obj_in = FileCreate(path=path, name=name, owner=user.id)
    obj_in = FileCreate(path=path, name=name, size=size, owner=16)
    exists = await file_crud.get(db=db, name=name)

    if exists:
        await file_crud.delete(db=db, name=name)

    response = await file_crud.create(db=db, obj_in=obj_in)
    return response  # Разобраться с ошибкой вывода (скорее всего, дело в типе поля datetime)
