# -*- coding: UTF-8 -*-
# vela was here
import time

import sqlalchemy
from app.common.exc import DataBaseCommitError
from configs.db_config import db
from configs.log_config import logger


class BaseModel(object):
    __undict__ = []

    @classmethod
    def create(cls, **kwargs):
        ret = cls()
        ret.update(data=kwargs)
        return ret

    def update(self, data):
        for k in data:
            if k != 'id':
                setattr(self, k, data[k])

        self.save()

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            logger.warning("DB", "sql commit error info", {'error': str(e)})
            db.session.rollback()
            raise DataBaseCommitError(400, '数据库提交错误，请检查是否填写完整')

    def save_session(self):
        db.session.add(self)

    @classmethod
    def save2db(cls):
        try:
            db.session.commit()
        except Exception as e:
            logger.warning("DB", "sql commit error info", {'error': str(e)})
            db.session.rollback()
            raise DataBaseCommitError(400, '数据库提交错误，请检查是否填写完整')

    def to_dict(self):
        # 读一下id属性，从而确保所有属性正确读入(载入)
        _id = self.id
        data_properties = {
            k: v
            for k, v in list(self.__dict__.items()) if k not in self.__undict__
                                                       and not isinstance(v, sqlalchemy.orm.state.InstanceState)
        }
        data_properties.update({
            k: getattr(self, k)
            for k, f in list(self.__class__.__dict__.items())
            if (k not in self.__undict__) and isinstance(f, property)
        })
        return data_properties

