from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from neutronstar import log
from neutronstar.common.constants import *
from neutronstar.crypto.crypto import Crypto


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def get_user(token: str = Depends(oauth2_scheme)):
    try:
        user = await Crypto.get_user(token=token)
    except Exception as e:
        log.error(f'get_user from token failed: e={e}')
        raise HTTP_401_EXCEPTION

    if not user:
        raise HTTP_401_EXCEPTION
    return user
