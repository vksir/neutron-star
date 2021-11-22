from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


class User(BaseModel):
    username: str


class UserInDB(User):
    hashed_password: str = Field(..., alias='password')


class Token(BaseModel):
    access_token: str = Field(...)
    token_type: str


class TokenData(BaseModel):
    sub: str = Field(..., description='username')