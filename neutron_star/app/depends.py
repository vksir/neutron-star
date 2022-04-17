from jose import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from neutron_star.app.models import User
from neutron_star.app.crypto import CRYPTO
from neutron_star.app.db.db import DB


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def get_user_depends_token(token: str = Depends(oauth2_scheme)) -> User:
    try:
        username = await CRYPTO.get_username_by_token(token=token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Signature has expired')
    user_in_db = await DB.get_user(username=username)
    if not user_in_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not registered')
    return User(**user_in_db.dict())
