# ! /usr/bin/env python
# -*- coding: UTF-8 -*-

from app.common.constants import ERROR_MSG_MAP
from flask import abort


class TableNotFound(Exception):
    def __init__(self, *args, **kwargs):
        super(TableNotFound, self).__init__(*args, **kwargs)


class DataBaseCommitError(Exception):
    def __init__(self, *args, **kwargs):
        super(DataBaseCommitError, self).__init__(*args, **kwargs)  # 调用父类的方法


class ApiError(Exception):
    def __init__(self, err_id, msg=None):
        if msg:
            super(ApiError, self).__init__(err_id, msg)
        else:
            super(ApiError, self).__init__(err_id, ERROR_MSG_MAP.get(err_id, "未定义错误"))
