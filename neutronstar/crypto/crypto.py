from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from neutronstar import log
from neutronstar.routes.models import User, UserInDB, TokenData
from neutronstar.db import DB


ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_DATS = 15
PASSWORD_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')


class Crypto:
    __instance = None
    __secret_key = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @property
    async def _secret_key(self):
        if self.__secret_key is None:
            self.__secret_key = await DB.get_user_password_secret_key()
        return self.__secret_key

    @classmethod
    async def get_access_token(cls, *, username: str, password: str):
        user_db = await DB.get_user(username=username)
        if not user_db:
            return None

        if not cls._verify_password(password, user_db.hashed_password):
            return None

        return await cls()._create_access_token(user_db.username)

    @classmethod
    async def register(cls, *, username: str, password: str):
        user_db = await DB.get_user(username=username)
        if user_db:
            log.info(f'register failed, username is exists: username={username}')
            return False

        is_success = await DB.add_user(username=username,
                                       password=cls._get_hashed_password(password))
        return is_success

    @classmethod
    async def get_user(cls, *, token: str):
        data = jwt.decode(token, await cls()._secret_key, algorithms=[ALGORITHM])
        token_data = TokenData(**data)

        user_db = await DB.get_user(username=token_data.username)
        if not user_db:
            raise Exception(f'get_user {token_data.username} from db failed')

        return User(**user_db.dict())

    async def _create_access_token(self, username: str):
        expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DATS)
        data = {
            'sub': username,
            'exp': expire
        }
        access_token = jwt.encode(data, await self._secret_key, algorithm=ALGORITHM)
        return access_token

    @staticmethod
    def _verify_password(password, hashed_password):
        return PASSWORD_CONTEXT.verify(password, hashed_password)

    @staticmethod
    def _get_hashed_password(password):
        return PASSWORD_CONTEXT.hash(password)
