# -*- coding: UTF-8 -*-
from flask import url_for
from flask_restplus import Api


class MyApi(Api):
    @property
    def specs_url(self):
        """Monkey patch for HTTPS"""
        scheme = 'http' if '5000' in self.base_url or '121.43.232.38' in self.base_url else 'https'
        return url_for(self.endpoint('specs'), _external=True, _scheme=scheme)


api = MyApi(
    title="接口文档",
    version="1.0",
    security=[""]
)
