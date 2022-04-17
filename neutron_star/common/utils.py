import os
import sys
import yaml
from neutron_star.common.constants import FilePath


def run_cmd(cmd: str):
    os.system(cmd)  # todo


def init_path():
    for path_name in dir(FilePath):
        path = getattr(FilePath, path_name)
        if (not path_name.endswith('HOME') and not path_name.endswith('DIR')) \
                or os.path.exists(path):
            continue
        run_cmd(f'mkdir -p {path}')


class CFGParser:
    def __init__(self):
        self._cfg = self._read()

    def get_db_account(self):
        if 'db_account' not in self._cfg \
                or 'username' not in self._cfg['db_account'] \
                or 'password' not in self._cfg['db_account'] \
                or 'host' not in self._cfg['db_account'] \
                or 'db_name' not in self._cfg['db_account']:
            print('DB_Account is not exists or is wrong')
            self._cfg['db_account'] = {
                'username': '',
                'password': '',
                'host': '',
                'db_name': ''
            }
            self._write(self._cfg)
            sys.exit()

        return self._cfg['db_account']['username'], \
            self._cfg['db_account']['password'], \
            self._cfg['db_account']['host'], \
            self._cfg['db_account']['db_name']

    @staticmethod
    def _read():
        cfg_path = FilePath.CFG_PATH
        if not os.path.exists(cfg_path):
            with open(cfg_path, 'w', encoding='utf-8') as f:
                yaml.dump({}, f)

        with open(cfg_path, 'r', encoding='utf-8') as f:
            return yaml.load(f, yaml.Loader)

    @staticmethod
    def _write(data: dict):
        cfg_path = FilePath.CFG_PATH
        with open(cfg_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f)
