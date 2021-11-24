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
    nick_name: Optional[str] = None

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
