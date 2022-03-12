# -*- coding: UTF-8 -*-

from flask_restplus import Namespace, Resource

from app.common.utils import sx_json
from app.service.update_data import CacheData

# cache_data = Namespace("CacheData", description="缓存数据")


# @cache_data.route("")
# class Cache(Resource):
#     def put(self):
#         """获取区域接口"""
#         res = CacheData.update_nv_data()
#         return sx_json(200, res)
