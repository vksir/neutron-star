import os
import platform
from fastapi import HTTPException, status


USER_HOME = os.environ['HOME'] if platform.system() == 'Linux' else os.environ['USERPROFILE']
HOME = f'{USER_HOME}/.ns'
CFG_PATH = f'{HOME}/cfg.yaml'
LOG_PATH = f'{HOME}//neutron-star.log'


TOKEN_TYPE_BEARER = 'bearer'
HTTP_401_EXCEPTION = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')