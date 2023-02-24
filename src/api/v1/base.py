from typing import Any, AnyStr, Dict, List

from fastapi import APIRouter, Depends, File, UploadFile, responses, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.users import verify_token
from src.core.config import app_settings
from src.db.db import get_session
from src.services.base import user_crud

router = APIRouter()


@router.get('/ping', response_model=AnyStr, status_code=status.HTTP_200_OK)
async def ping(db: AsyncSession = Depends(get_session), user: bool = Depends(verify_token)) -> Any:

    return 'dsadsa'
