from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from neutron_star.app.models import User, TokenData
from neutron_star.app.db.db import DB


ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_DATS = 15
PASSWORD_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')


class Crypto:
    def __init__(self):
        self.__user_password_secret_key = None
        self.__host_root_password_secret_key = None

    @property
    async def _user_password_secret_key(self):
        if self.__user_password_secret_key is None:
            self.__user_password_secret_key = await DB.get_user_password_secret_key()
        return self.__user_password_secret_key

    @property
    async def _host_root_password_secret_key(self):
        if self.__host_root_password_secret_key is None:
            self.__host_root_password_secret_key = await DB.get_host_root_password_secret_key()
        return self.__host_root_password_secret_key

    async def get_username_by_token(self, *, token: str):
        data = jwt.decode(token, await self._user_password_secret_key, algorithms=[ALGORITHM])
        token_data = TokenData(**data)
        return token_data.username

    async def create_access_token(self, username: str):
        expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DATS)
        data = {
            'sub': username,
            'exp': expire
        }
        access_token = jwt.encode(data, await self._user_password_secret_key, algorithm=ALGORITHM)
        return access_token

    @staticmethod
    async def verify_password(password: str, hashed_password: str):
        return PASSWORD_CONTEXT.verify(password, hashed_password)

    @staticmethod
    async def get_hashed_password(password: str):
        return PASSWORD_CONTEXT.hash(password)


CRYPTO = Crypto()
