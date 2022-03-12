# -*- coding: utf-8 -*-
# vela was here
import inspect
import time
from collections import defaultdict
from functools import wraps

import expiringdict
from flask import jsonify

from app.common.constants import ERROR_MSG_MAP

timer_counts = defaultdict(int)


def sx_json(code, ret_data=None, msg=None, extra_data=None):
    """ 统一格式返回 """
    return jsonify({
        "code":
            code,
        "msg":
            ERROR_MSG_MAP.get(code) if msg is None else msg,
        "data":
            ret_data,
        "extra_data": extra_data
    })


def time_it(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        st = time.time()
        ret = func(*args, **kwargs)
        dt = time.time() - st
        endpoint = '{}.{}'.format(func.__module__, func.__name__)
        timer_counts[endpoint] += 1
        print('{}[{}] finished, exec {}s'.format(endpoint, '%05d' % timer_counts[endpoint], round(dt, 4)))
        return ret

    return wrapper


expiringdict_caches = {}


def SXCache(exp_time=100):
    def wrapper0(func):
        def wrapper(*args, **kwargs):
            nor_args_str, all_args = normalize_args(func, args, kwargs)
            key = 'sx_cache:{}:{}'.format(func.__name__, nor_args_str)
            key = str(key)
            ret = None
            cache_key = func.__module__ + '.' + func.__name__
            if cache_key not in expiringdict_caches.keys():
                expiringdict_caches[cache_key] = expiringdict.ExpiringDict(max_len=3000, max_age_seconds=exp_time)
            cache = expiringdict_caches[cache_key]
            if cache.get(key, None) is not None:
                value = cache.get(key)
                ret = value
                cache[key] = ret
            else:
                spec = inspect.getargs(func.__code__).args
                all_args = kwargs
                all_args.update(dict(zip(spec, args)))
                ret = func(**all_args)
                cache[key] = ret
            return ret

        return wrapper

    return wrapper0


def normalize_args(func, args, kwargs):
    spec = inspect.getargs(func.__code__).args
    all_args = {}
    all_args.update(get_default_args(func))
    all_args.update(dict(zip(spec, args)))
    all_args.update(kwargs)  # 三者顺序不能变，否则参数会变成默认值
    res_all_args = {k: v for k, v in all_args.items()}
    all_args.pop('cache_permanent', None)
    all_args_str = f'{tuple(sorted(all_args.items()))}'
    return all_args_str, res_all_args


def get_default_args(func):
    signature = inspect.signature(func)
    return {
        k: v.default
        for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty
    }


def format_float(floats):
    """格式化小数为百分数"""
    return '{:.2%}'.format(floats)
