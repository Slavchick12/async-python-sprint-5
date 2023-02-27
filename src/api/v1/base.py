import time
from typing import Any, Dict

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.users import verify_token
from src.core.config import app_settings
from src.db.db import get_session

router = APIRouter()


@router.get('/ping', response_model=Dict, status_code=status.HTTP_200_OK)
async def ping(db: AsyncSession = Depends(get_session), user: bool = Depends(verify_token)) -> Any:
    """
    Get service versions.
    """
    try:
        start = time.time()
        connect = await db.connection()
        db_ping = time.time() - start

        if connect:
            return {app_settings.DB_CONNECTION: db_ping}

    except Exception:
        return {app_settings.DB_CONNECTION: app_settings.NO_ACCESS}
