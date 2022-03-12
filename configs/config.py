# -*- coding: utf-8 -*-
# vela was here

import base64
import yaml
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__)).split('/')[:-1]
BASEDIR = '/'.join(BASEDIR)


class Config(object):
    """ 基础配置 """
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_POOL_SIZE = 6
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_MAX_OVERFLOW = 2
    SQLALCHEMY_POOL_RECYCLE = 600
    SQLALCHEMY_POOL_TIMEOUT = 60
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_pre_ping': True}
    # 打印sql
    SQLALCHEMY_ECHO = False

    def __init__(self):
        # f'{os.environ["FLASK_ENV"]}.yaml'
        env_config = yaml.load(open('development.yaml'), Loader=yaml.SafeLoader)
        self.__dict__ = dict(self.__dict__, **env_config)
        self._config()

    def _config(self):
        self.mysql['password'] = self.mysql['password']
        self.SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}".format(
            self.mysql['username'], self.mysql['password'], self.mysql['host'],
            self.mysql['port'], self.mysql['database'])


current_config = Config()


