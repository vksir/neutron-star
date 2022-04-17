import os
import platform


class Constants:
    TOKEN_TYPE_BEARER = 'bearer'


class FilePath:
    HOME = os.environ['HOME'] if platform.system() == 'Linux' else os.environ['USERPROFILE']
    CFG_DIR = f'{HOME}/.ns'
    CFG_PATH = f'{CFG_DIR}/cfg.yaml'
    LOG_PATH = f'{CFG_DIR}/neutron_star.log'
