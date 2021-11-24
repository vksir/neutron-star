import datetime
import databases
from sqlalchemy import select, insert
from app.db.schemas import *
from app.routes import models
from app import log
from app.common.utils import CFGParser


class DB:
    __instance = None
    _database = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance._init()
        return cls.__instance

    def _init(self):
        cfg_parser = CFGParser()
        username, password, host, db_name = cfg_parser.get_db_account()
        databases_sql = f'postgresql://{username}:{password}@{host}/{db_name}'
        self._database = databases.Database(databases_sql)

    @classmethod
    async def connect(cls):
        await cls()._database.connect()

    @classmethod
    async def disconnect(cls):
        await cls()._database.disconnect()

    @classmethod
    async def get_user(cls, *, username: str):
        sql = select(User).where(User.username == username)
        row = await cls()._database.fetch_one(sql)
        if not row:
            return None
        return models.UserInDB(**row)

    @classmethod
    async def add_user(cls, *, username: str, password: str):
        sql = insert(User).values(username=username,
                                  password=password,
                                  register_date=datetime.datetime.now())
        try:
            await cls()._database.execute(sql)
            return True
        except Exception as e:
            log.error(f'try add_user into db failed: username={username}, e={e}')
        return False

    @classmethod
    async def get_user_password_secret_key(cls):
        sql = select(Dictionary).where(Dictionary.key == 'user_password_secret_key')
        row = await cls()._database.fetch_one(sql)
        return models.Dictionary(**row).value
