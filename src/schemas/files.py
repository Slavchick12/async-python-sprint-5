from datetime import datetime

from pydantic import BaseModel


class FileBase(BaseModel):
    path: str
    size: int
    owner: int


class FileCreate(FileBase):
    name: str
    owner: int


class FileInDBBase(FileBase):
    id: int
    name: str
    created_at: datetime
    is_downloadable: bool
