from typing import Any, AnyStr, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import Base
from src.models.models import User, File


ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class Repository:

    def get(self, *args, **kwargs):
        raise NotImplementedError

    def get_multi(self, *args, **kwargs):
        raise NotImplementedError

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError


class RepositoryDB(Repository, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self._model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        statement = select(self._model).where(self._model.id == id)
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()

    async def get_multi(self, db: AsyncSession, *, skip=0, limit=100) -> List[ModelType]:
        statement = select(self._model).offset(skip).limit(limit)
        results = await db.execute(statement=statement)
        return results.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self._model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, *, id: int, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        pass

    async def delete(self, db: AsyncSession, *, id: int) -> ModelType:
        pass


class UserDB(RepositoryDB[ModelType, CreateSchemaType, UpdateSchemaType]):
    async def get(self, db: AsyncSession, name: AnyStr, password: AnyStr) -> Optional[ModelType]:
        statement = select(self._model).where(self._model.name == name).where(self._model.password == password)
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()

    async def get_token(self, db: AsyncSession, token: AnyStr) -> Optional[ModelType]:
        statement = select(self._model).where(self._model.token == token)
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()

    async def update(
        self, db: AsyncSession, *, name: AnyStr, token: AnyStr
    ) -> ModelType:
        statement = update(self._model).where(self._model.name == name).values(token=token)
        await db.execute(statement=statement)
        await db.commit()


class FileDB(RepositoryDB[ModelType, CreateSchemaType, UpdateSchemaType]):
    async def get(self, db: AsyncSession, name: AnyStr) -> Optional[ModelType]:
        statement = select(self._model).where(self._model.name == name)
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()

    async def delete(self, db: AsyncSession, *, name: AnyStr) -> ModelType:
        statement = delete(self._model).where(self._model.name == name)
        await db.execute(statement=statement)
        await db.commit()


user_crud = UserDB(User)
file_crud = FileDB(File)
