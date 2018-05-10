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
from service import power
from service import balance
from service import produce
import log
import md5
import time
import random
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

HIST_PAGE = 20

VAL_PWER_REG = 25
VAL_PWER_LOGIN = 1

VAL_COIN_REG = 10


@gen.coroutine
def reg_bonus(mid):
    # add power
    yield power.change(mid, power.PW_TYPE_REG, VAL_PWER_REG, "新用户算力值增加")
    # add balance
    yield balance.change(mid, balance.BL_TYPE_REG, VAL_COIN_REG, "新用户派发")
    # init mine
    yield produce.refresh_mine(mid)
    raise gen.Return({'ret': 1})


@gen.coroutine
def login_bonus(mid):
    # add power
    ret = yield power.change(mid, power.PW_TYPE_LOGIN, VAL_PWER_LOGIN, "登陆算力值增加")
    raise gen.Return(ret)


@gen.coroutine
def collect_coin(mid):
    # first collect from produce col
    ret = yield produce.collect_coin(mid)
    if ret.get('ret') != 1:
        raise gen.Return(ret)

    # change for balance
    log.info("mine.collect_coin@produce ret:" + ujson.dumps(ret, ensure_ascii=False))
    val = ret.get('data').get('coin')
    ret_balance = yield balance.change(mid, balance.BL_TYPE_MINE, val, "挖矿收益")
    if ret_balance.get('ret') != 1:
        log.error(str(mid) + "@mine.collect_coin@need rollback@produce ret:" + ujson.dumps(ret_balance, ensure_ascii=False) +
                  ", failed upon balance change, ret:" + ujson.dumps(ret_balance, ensure_ascii=False))
        raise gen.Return(ret_balance)

    # refresh mine if succeed
    yield produce.refresh_mine(mid)
    raise gen.Return(ret)


@gen.coroutine
def info(mid):
    mid = int(mid)
    col_mine = get_col_mine_mine()
    doc = yield motordb.mongo_find_one(col_mine, {'_id': mid})
    if doc is False:
        log.error('mine.info@query col_produce, mid:%s' % mid)
        raise gen.Return({'ret': -1, 'data': {'msg': '服务器忙，请稍后再试吧~'}})
    if not doc:
        log.warning('mine.info@not reg, mid:%s' % mid)
        raise gen.Return({'ret': -1, 'data': {'msg': '您还未注册~'}})

    produce_info = doc.get('produce')
    if produce_info:
        produce.build_produce_info(produce_info)

    del doc['_id']
    raise gen.Return({'ret': 1, 'data': doc})
