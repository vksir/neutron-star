import datetime
import asyncpg
import uuid
from typing import Union
from neutron_star.app.models import UserInDB
from neutron_star.app.models import Dictionary
from neutron_star.app.models import HostInDB
from neutron_star.common.utils import CFGParser


class DataBase:
    class DataBaseException(Exception):
        pass

    def __init__(self):
        cfg_parser = CFGParser()
        username, password, host, db_name = cfg_parser.get_db_account()
        self._dsn = f'postgresql://{username}:{password}@{host}/{db_name}'
        self._db = None

    async def connect(self):
        self._db = await asyncpg.create_pool(self._dsn, max_size=16)

    async def disconnect(self):
        await self._db.close()

    async def _get_key_value_from_db(self, key):
        row = await self._db.fetchrow('select * from t_dictionary where key = $1', key)
        return Dictionary(**row).value

    async def get_user(self, *, username: str):
        row = await self._db.fetchrow('select * from t_user where username = $1', username)
        if not row:
            return None
        return UserInDB(**row)

    async def add_user(self, *, username: str, password: str):
        await self._db.execute('insert into t_user (username, password, register_date) '
                               'values ($1, $2, $3)',
                               username, password, datetime.datetime.now())

    async def get_user_password_secret_key(self):
        return await self._get_key_value_from_db('user_password_secret_key')

    async def get_hosts(self, *, username: str):
        rows = await self._db.fetch('select * from t_host where username = $1', username)
        if not rows:
            return []
        return [HostInDB(**row) for row in rows]

    async def _get_unique_host_uuid(self) -> str:
        while True:
            host_uuid = str(uuid.uuid4())
            row = await self._db.fetchrow('select * from t_host where uuid = $1', host_uuid)
            if not row:
                return host_uuid

    async def add_host(self, *,
                       ip: str,
                       port: int,
                       root_password: str,
                       username: str,
                       nickname: Union[str, None]):
        host_uuid = await self._get_unique_host_uuid()
        if nickname is None:
            nickname = host_uuid
        await self._db.execute('insert into t_host (uuid, ip, port, root_password, username, nickname) '
                               'values ($1, $2, $3, $4, $5, $6)',
                               host_uuid, ip, port, root_password, username, nickname)

    async def delete_host(self, *, host_uuid: str, username: str):
        await self._db.execute('delete from t_host where uuid = $1 and username = $2', host_uuid, username)


DB = DataBase()
