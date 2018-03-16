# -*- coding:utf-8 -*-
import time
import random
import urllib2
import ujson
from tornado import gen
from lib import motordb
from lib import call
from lib.db import get_redis
from lib.db import *
from config import config
import log
import md5
import time
import random
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

@gen.coroutine
def add_app(app):
    col = get_col_app_info()
    doc = yield motordb.mongo_find_one(col, {'_id': app['_id']})
    if doc:
        raise gen.Return({'ret':-1, 'data': {'msg': '此app已入库'}})
    ret = yield motordb.mongo_insert_one(col, app)

    if not ret:
        raise gen.Return({'ret':-1, 'data': {'msg': '添加app失败', 'app': app}})

    raise gen.Return({'ret':1, 'data': {'msg': '添加成功'}})


@gen.coroutine
def account_hello(phone):
    raise gen.Return({'ret':1, 'ph': phone})

