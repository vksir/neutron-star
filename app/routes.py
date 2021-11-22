from fastapi import FastAPI, Response, Request, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.log import log
from app.constants import *
from app.models import *
from app.crypto import *


app = FastAPI(title='NEUTRON STAR', version='0.1.0')


@app.middleware('http')
async def middleware(request: Request, call_next, user: User = Depends(get_user_from_token)):
    request.scope['token_data'] = {'sub': 'name'}
    print(user)
    response = await call_next(request)
    return response


@app.get('/test')
async def test(request: Request):
    return {
        'msg': 'Hello, I am Neutron Star.',
        'method': request.method,
        'content-type': request.headers.get('content-type'),
        'params': request.path_params,
        'body': await request.body()
    }


@app.post('/token', response_model=Token)
async def get_token_by_login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = verify_user(form_data)
    if not user:
        raise HTTP_401_EXCEPTION
    access_token = create_access_token(user.username)
    return Token(access_token=access_token, token_type='bearer')


@app.get('/users/me')
async def read_users_me(request: Request, current_user: User = Depends(get_user_from_token)):
    print(current_user)
    return current_user

