from typing import List
from fastapi import APIRouter
from fastapi import Response
from fastapi import Depends
from pydantic import BaseModel
from neutron_star.app.models import User
from neutron_star.app.models import Host
from neutron_star.app.models import HostInDB
from neutron_star.app.db.db import DB
from neutron_star.app.depends import get_user_depends_token


router = APIRouter(tags=['host'])


class HostAdd(BaseModel):
    ip: str
    port: int
    nickname: str = None
    root_password: str


class HostUpdate(BaseModel):
    port: int = None
    nickname: str = None
    root_password: str = None


@router.get('/host', response_model=List[Host], summary='获取用户拥有的主机')
async def get_hosts(user: User = Depends(get_user_depends_token)):
    hosts_in_db = await DB.get_hosts(username=user.username)
    return [Host(**host_in_db.dict()) for host_in_db in hosts_in_db]


@router.post('/host', summary='增加用户主机')
async def add_host(host: HostAdd, user: User = Depends(get_user_depends_token)):
    await DB.add_host(ip=host.ip,
                      port=host.port,
                      root_password=host.root_password,
                      username=user.username,
                      nickname=host.nickname)
    return Response()


@router.delete('/host/{uuid}', summary='删除用户主机')
async def delete_host(uuid: str, user: User = Depends(get_user_depends_token)):
    await DB.delete_host(host_uuid=uuid, username=user.username)
    return Response()
