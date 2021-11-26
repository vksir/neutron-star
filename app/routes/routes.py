from fastapi import Request, Depends, Response, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app import app
from app.common.constants import *
from app.crypto.crypto import Crypto
from app.db import DB
from app.routes.models import *
from app.routes import depends


@app.on_event('startup')
async def startup():
    await DB.connect()


@app.on_event('shutdown')
async def shutdown():
    await DB.disconnect()


@app.middleware('http')
async def middleware(request: Request, call_next):
    response = await call_next(request)
    return response


@app.get('/test')
async def test(request: Request):
    return {
        'msg': 'Hello, I am Neutron Star.',
        'method': request.method,
        'content-type': request.headers.get('content-type'),
        'params': request.query_params,
        'body': await request.body()
    }


@app.post('/token', response_model=Token, summary='获取令牌')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    access_token = await Crypto.get_access_token(username=form_data.username,
                                                 password=form_data.password)
    if not access_token:
        raise HTTP_401_EXCEPTION
    return Token(access_token=access_token, token_type=TOKEN_TYPE_BEARER)


@app.post('/register', response_model=None, summary='注册')
async def register(form_data: OAuth2PasswordRequestForm = Depends(),
                   # ):
                   user: User = Depends(depends.get_user)):
    if user.username != 'vksir':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='暂不开放注册')

    is_success = await Crypto.register(username=form_data.username,
                                       password=form_data.password)
    if not is_success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='用户名已注册')
    return Response()


@app.get('/users/me')
async def read_me(user: User = Depends(depends.get_user)):
    return user



