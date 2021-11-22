from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt
from app.constants import *
from app.models import *


SECRET_KEY = 'aff10e322f09d7f9e29df8cb8da4aaa4fbb9738e9b63cc156799aabf71cb08e1'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(password, hashed_password):
    return password_context.verify(password, hashed_password)


def get_hashed_password(password):
    return password_context.hash(password)


users_db = {
    'vksir': {
        'username': 'vksir',
        'password': get_hashed_password('4578')
    }
}


def get_user_from_db(username):
    if username not in users_db:
        return None
    return UserInDB(**users_db[username])


def verify_user(form_data: OAuth2PasswordRequestForm):
    user_db = get_user_from_db(form_data.username)
    if not user_db:
        return None
    if not verify_password(form_data.password, user_db.hashed_password):
        return None
    return user_db


def create_access_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {
        'sub': username,
        'exp': expire
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return access_token


async def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenData(**data)
    except Exception as e:
        log.info('get token_data failed')
        raise HTTP_401_EXCEPTION
    user_db = get_user_from_db(token_data.sub)
    if not user_db:
        raise HTTP_401_EXCEPTION
    return user_db