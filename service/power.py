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
def account_hello(phone):
    raise gen.Return({'ret':1, 'ph': phone})


PW_TYPE_REG = 1
PW_TYPE_LOGIN = 2


@gen.coroutine
def add_change_hist(mid, ty, val, desc):
    col_hist = get_col_mine_power_history()
    tnow = int(time.time())
    today = int(time.strftime("%Y%m%d", time.localtime(time.time())))
    # todo: high level concorrency attack
    if ty == PW_TYPE_REG:
        # check whether already registered
        doc = yield motordb.mongo_find_one(col_hist, {'mid': mid, 'type': ty})
        if doc:
            log.warn("power.add_change_hist@suspected reg attack, mid:%s already registered" % mid)
            raise gen.Return(False)

        if doc is False:
            log.error("power.add_change_hist@db error@check whether already registered")
            raise gen.Return(False)

        ret = yield motordb.mongo_insert_one(col_hist, {'mid': mid, 'type': ty, 'val': val, 'desc': desc, 'ct': tnow, 'day': today})
        if not ret:
            raise gen.Return(False)

    elif ty == PW_TYPE_LOGIN:
        # check whether login today
        doc = yield motordb.mongo_find_one(col_hist, {'mid': mid, 'type': ty, 'day': today})
        if doc:
            raise gen.Return(False)
        if doc is False:
            log.error("power.add_change_hist@db error@check whether login today")
            raise gen.Return(False)

        ret = yield motordb.mongo_insert_one(col_hist, {'mid': mid, 'type': ty, 'val': val, 'desc': desc, 'ct': tnow, 'day': today})
        if not ret:
            log.error("power.add_change_hist@db error@insert login bonus failed, duplicate?")
            raise gen.Return(False)

    else:
        raise gen.Return(False)

    raise gen.Return(True)


@gen.coroutine
def change(mid, ty, val, desc):
    mid = int(mid)
    ty = int(ty)
    val = float(val)
    desc = str(desc)
    valid = yield add_change_hist(mid, ty, val, desc)
    if not valid:
        raise gen.Return({'ret': -1})

    # add into mine.power
    tnow = int(time.time())
    col_mine = get_col_mine_mine()

    # insert it if not exists
    doc = yield motordb.mongo_find_one_and_update(col_mine, {'_id': mid}, {'$inc': {'power': val}, '$set': {'ut': tnow}}, upsert=True)
    if not doc:
        raise gen.Return({'ret': -1, 'data': {'msg': '服务器忙，请稍后再试吧~'}})

    power = doc.get('power', 0)
    raise gen.Return({'ret': 1, 'data': {'power': power}})


