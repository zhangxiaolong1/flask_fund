# -*- coding: utf-8 -*-
import os

from configs.api_config import api
from configs.config import current_config
from configs.db_config import db


os.environ['TZ'] = 'Asia/Shanghai'


def create_app(app):
    app.config.from_object(current_config)
    app.config["PROPAGATE_EXCEPTIONS"] = False
    db.init_app(app)
    api.init_app(app)

    # from app.router.cache_data import cache_data
    # api.add_namespace(cache_data, path="/cache")

    from app.router.fund_func import fund_func
    api.add_namespace(fund_func, path="/fund_func")

    return app
