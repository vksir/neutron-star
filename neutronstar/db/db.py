import datetime
import asyncpg
from neutronstar.routes.models import UserInDB, Dictionary
from neutronstar import log
from neutronstar.common.utils import CFGParser


class DB:
    __instance = None
    _db = None
    _dsn = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance._init()
        return cls.__instance

    def _init(self):
        cfg_parser = CFGParser()
        username, password, host, db_name = cfg_parser.get_db_account()
        self._dsn = f'postgresql://{username}:{password}@{host}/{db_name}'

    @classmethod
    async def connect(cls):
        cls()._db = await asyncpg.create_pool(cls()._dsn, max_size=16)

    @classmethod
    async def disconnect(cls):
        await cls()._db.close()

    @classmethod
    async def get_user(cls, *, username: str):
        row = await cls()._db.fetchrow('select * from t_user where username = $1', username)
        if not row:
            return None
        return UserInDB(**row)

    @classmethod
    async def add_user(cls, *, username: str, password: str):
        try:
            await cls().execute('insert into t_user (username, password, register_date) '
                                'values ($1, $2, $3)', username, password,
                                datetime.datetime.now())
            return True
        except Exception as e:
            log.error(f'try add_user into db failed: username={username}, e={e}')
        return False

    @classmethod
    async def get_user_password_secret_key(cls):
        row = await cls()._db.fetchrow('select * from t_dictionary where key = $1',
                                       'user_password_secret_key')
        return Dictionary(**row).value
