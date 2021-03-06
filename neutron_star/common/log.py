import logging
from neutron_star.common.constants import FilePath


log = logging.getLogger(__name__)
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(filename)s] %(message)s')
log.setLevel(logging.DEBUG)


def init_log():
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    sh.setLevel(logging.DEBUG)
    fh = logging.FileHandler(FilePath.LOG_PATH, 'w', encoding='utf-8')
    fh.setFormatter(formatter)
    fh.setLevel(logging.DEBUG)
    log.addHandler(sh)
    log.addHandler(fh)





