# -*- coding:utf-8 -*-
"""
治理员业务逻辑
"""
import time
import random
import urllib2
import ujson
from tornado import gen
from lib import motordb
from lib import call
from lib.db import get_redis
from lib.db import get_col_account_member
from config import config
import log

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def phone_verifycode_cache_key(phone):
    return str(phone) + "_verify"


@gen.coroutine
def add_phone(phone):
    phone = int(phone)
    phone_str = str(phone)
    col = get_col_account_member()
    doc = yield motordb.mongo_find_one(col, {'phone': phone})
    if doc is False:
        log.error("db failed")
        raise gen.Return({'ret': -1001, 'data': {'msg': "服务器正忙，请稍后再试吧"}})

    if doc:
        raise gen.Return({'ret': -1002, 'data': {'msg': "此手机号已经注册"}})

    cache = get_redis()
    verify_key = cache.get(phone_str)
    if verify_key:
        raise gen.Return({'ret': -1003, 'data': {'msg': "此手机号已经获取了验证码，请稍后再获取吧"}})

    # call
    #  resp = yield call.async_post(config.url_phone_verify_code, {'phone': phone}, retjson=False)
    verify_code = '123433'

    cache_key = phone_verifycode_cache_key(phone)
    cache.set(cache_key, verify_code)
    cache.ttl(cache_key, 60)
    raise gen.Return({'ret': 1, 'data': {'code': verify_code}})


@gen.coroutine
def account_hello(phone):
    raise gen.Return({'ret':1, 'ph': phone})