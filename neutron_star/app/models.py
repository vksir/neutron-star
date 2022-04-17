from enum import Enum
from typing import Optional
from datetime import date
from pydantic import BaseModel, Field


class Sex(Enum):
    MAN = 'man'
    WOMAN = 'woman'


class User(BaseModel):
    username: str
    register_date: date
    birthday: Optional[date] = None
    sex: Optional[Sex] = None
    nickname: Optional[str] = None

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str = Field(..., alias='password')


class Token(BaseModel):
    access_token: str = Field(...)
    token_type: str


class TokenData(BaseModel):
    username: str = Field(..., alias='sub')


class Dictionary(BaseModel):
    key: str = Field(...)
    value: Optional[str] = None


class Host(BaseModel):
    uuid: str
    ip: str
    port: int
    username: str
    nickname: str

    class Config:
        orm_mode = True


class HostInDB(Host):
    root_password: str = Field(..., alias='root_password')
