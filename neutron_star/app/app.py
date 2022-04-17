import logging
from fastapi import FastAPI
from neutron_star.common.utils import init_path
from neutron_star.common.log import log
from neutron_star.common.log import init_log
from neutron_star.app.routes import routes
from neutron_star.app.routes import user_routes
from neutron_star.app.routes import host_routes


init_path()
init_log()
log.setLevel(logging.DEBUG)
app = FastAPI(title='NEUTRON STAR', version='0.1.0')
app.include_router(routes.router)
app.include_router(user_routes.router)
app.include_router(host_routes.router)
