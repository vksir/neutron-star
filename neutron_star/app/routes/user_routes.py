from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from neutron_star.common.constants import Constants
from neutron_star.app.models import Token
from neutron_star.app.models import User
from neutron_star.app.depends import get_user_depends_token
from neutron_star.app.db.db import DB
from neutron_star.app.crypto import CRYPTO


router = APIRouter(tags=['user'])


@router.post('/user/token', response_model=Token, summary='获取令牌')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_in_db = await DB.get_user(username=form_data.username)
    if not user_in_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not registered')
    if not await CRYPTO.verify_password(password=form_data.password, hashed_password=user_in_db.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect password')

    access_token = await CRYPTO.create_access_token(form_data.username)
    return Token(access_token=access_token, token_type=Constants.TOKEN_TYPE_BEARER)


@router.post('/user/register', summary='注册')
async def register(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != 'vksir':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='暂不开放注册')
    user_in_db = await DB.get_user(username=form_data.username)
    if user_in_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User is registered')

    hashed_password = await CRYPTO.get_hashed_password(form_data.password)
    await DB.add_user(username=form_data.username, password=hashed_password)
    return Response()


@router.get('/user/me', response_model=User, summary='获取个人信息')
async def read_me(user: User = Depends(get_user_depends_token)):
    return user
