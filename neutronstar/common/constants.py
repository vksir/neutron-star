import os
import platform
from fastapi import HTTPException, status


HOME = os.environ['HOME'] if platform.system() == 'Linux' else os.environ['USERPROFILE']
CFG_DIR = f'{HOME}/.ns'
CFG_PATH = f'{CFG_DIR}/cfg.yaml'
LOG_PATH = f'{CFG_DIR}/neutron_star.log'


TOKEN_TYPE_BEARER = 'bearer'
HTTP_401_EXCEPTION = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')