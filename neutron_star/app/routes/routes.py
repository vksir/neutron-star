import httpx
from fastapi import Request
from fastapi import Depends
from fastapi import Response
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from fastapi import Header
from neutron_star.app.db.db import DB
from neutron_star.app.models import User
from neutron_star.app.depends import get_user_depends_token


router = APIRouter()


@router.on_event('startup')
async def startup():
    await DB.connect()


@router.on_event('shutdown')
async def shutdown():
    await DB.disconnect()


@router.route('/test/{path:path}', methods=['get', 'post'])
async def test(request: Request, path):
    return {
        'msg': 'Hello, I am Neutron Star.',
        'base_url': request.base_url,
        'url': request.url,
        'path': path,
        'params': request.query_params,
        'method': request.method,
        'headers': request.headers,
        'body': await request.body()
    }


@router.get('/api/{path:path}')
@router.post('/api/{path:path}')
@router.put('/api/{path:path}')
@router.delete('/api/{path:path}')
async def dst_run(req: Request,
                  uuid: str = Header(...),
                  component: str = Header(...),
                  user: User = Depends(get_user_depends_token)):
    hosts_in_db = await DB.get_hosts(username=user.username)
    target_hosts_in_db = [host_in_db for host_in_db in hosts_in_db if host_in_db.uuid == uuid]
    if not target_hosts_in_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Uuid not exists')
    if len(target_hosts_in_db) != 1:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Same uuid exists')
    target_host_in_db = target_hosts_in_db[0]
    ip = target_host_in_db.ip

    port_map = {
        'dst_run': 5800
    }
    if component not in port_map:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid component')
    port = port_map[component]

    method = req.method
    path = req.path_params['path']
    headers = dict(req.headers)
    body = await req.body()

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.request(
                method=method,
                url=f'http://{ip}:{port}/{path}?{req.query_params}',
                headers=headers,
                content=body,
                timeout=30
            )
    except Exception as e:
        return Response(content=e,
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(content=resp.content,
                    status_code=resp.status_code,
                    headers=resp.headers)
