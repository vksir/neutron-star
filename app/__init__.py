import logging
from importlib import import_module
from fastapi import FastAPI
from app.common.utils import init_path
from app.common.log import log, init_log


init_path()
init_log()
log.setLevel(logging.DEBUG)
app = FastAPI(title='NEUTRON STAR', version='0.1.0')
import_module('app.routes.plugins.dst_run.routes')
import_module('app.routes.routes')