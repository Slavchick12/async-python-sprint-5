import secrets
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import app_settings
from src.db.db import get_session
from src.schemas.users import UserCreate, UserGet
from src.services.base import user_crud

router = APIRouter()


@router.post('/register', response_model=Dict, status_code=status.HTTP_201_CREATED)
async def register(db: AsyncSession = Depends(get_session), obj: UserCreate = None) -> Any:
    """
    User register.
    """
    app_settings.Logger.wb_logger.info(app_settings.USER_REGISTER)
    response = dict()

    try:
        user = await user_crud.create(db=db, obj_in=obj)
        name = user.name
        password = user.password

        response['name'] = name
        response['password'] = password
        app_settings.Logger.wb_logger.info(app_settings.USER_CREATED.format(name=name))
    except IntegrityError:
        response[obj.name] = 'This name already exists'
        app_settings.Logger.wb_logger.info(app_settings.NAME_EXISTS)

    return response


@router.post('/auth', response_model=Dict, status_code=status.HTTP_200_OK)
async def authentication(db: AsyncSession = Depends(get_session), obj: UserGet = None) -> Any:
    """
    User authentication.
    """
    app_settings.Logger.wb_logger.info(app_settings.USER_AUTH)
    response = dict()

    user = await user_crud.get(db=db, name=obj.name, password=obj.password)

    if user is None:
        response['name'] = app_settings.INVALID_NAME_OR_PASS
        app_settings.Logger.wb_logger.info(app_settings.INVALID_NAME_OR_PASS)
        return response

    new_token = secrets.token_hex(20)

    await user_crud.update(db=db, name=user.name, token=new_token)
    app_settings.Logger.wb_logger.info(app_settings.TOKEN_WAS_GENERATED)

    response['token'] = new_token
    return response


async def verify_token(db: AsyncSession = Depends(get_session), req: Request = None):
    token = req.headers.get('Authorization')

    if not token:
        raise HTTPException(status_code=401, detail=app_settings.UNATHORIZED)

    user = await user_crud.get_token(db=db, token=token)

    if not user:
        raise HTTPException(status_code=401, detail=app_settings.UNATHORIZED)

    return user
