from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    password: str


class UserGet(UserBase):
    pass


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserInDBBase(UserBase):
    id: int


class UserInDB(UserInDBBase):
    pass
