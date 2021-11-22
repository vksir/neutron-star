import logging


log = logging.getLogger()
log.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(filename)s]')


sh = logging.StreamHandler()
sh.setFormatter(formatter)
fh = logging.FileHandler('log.log', 'w', encoding='utf-8')
fh.setFormatter(formatter)
log.addHandler(sh)
log.addHandler(fh)





