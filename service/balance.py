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

HIST_PAGE = 20
BL_TYPE_REG = 1  # 注册
BL_TYPE_LOGIN = 2  # 登陆
BL_TYPE_MINE = 3  # 挖矿
BL_TYPE_DOWNLOAD_APP = 11  # 下载
BL_TYPE_VIEW_NEWS = 12  # 看咨询

@gen.coroutine
def add_change_hist(mid, ty, val, desc):
    para = 'mid:%s, type:%s, val:%s, desc:%s' % (mid, ty, val, desc)
    if not mid or not ty or not val:
        raise gen.Return({'ret': -1, 'data': {'msg': '参数错误'}})

    col_hist = get_col_mine_balance_history()
    tnow = int(time.time())
    if ty == BL_TYPE_REG:
        # check whether already registered
        doc = yield motordb.mongo_find_one(col_hist, {'mid': mid, 'type': ty})
        if doc:
            log.warn("balance.add_change_hist@uspected reg attack@already registered: " + para)
            raise gen.Return(False)

        if doc is False:
            log.error("balance.add_change_hist@db error@check whether already registered: "+ para)
            raise gen.Return(False)

    elif ty == BL_TYPE_LOGIN:
        # check whether login today
        today = int(time.strftime("%Y%m%d", time.localtime(time.time())))
        doc = yield motordb.mongo_find_one(col_hist, {'mid': mid, 'type': ty, 'day': today})
        if doc:
            raise gen.Return(False)
        if doc is False:
            log.error("balance.add_change_hist@db error@check whether login today:" + para)
            raise gen.Return(False)

    elif ty != BL_TYPE_MINE:
        log.error("balance.add_change_hist@unrecognized change: " + para)
        raise gen.Return(False)

    ret = yield motordb.mongo_insert_one(col_hist, {'mid': mid, 'type': ty, 'val': val, 'desc': desc, 'ct': tnow})
    if not ret:
        raise gen.Return(False)

    raise gen.Return(True)


@gen.coroutine
def change(mid, ty, val, desc):
    if not mid or not ty or not val:
        raise gen.Return({'ret': -1, 'data': {'msg': '参数错误'}})

    mid = int(mid)
    ty = int(ty)
    val = float(val)
    desc = str(desc)
    valid = yield add_change_hist(mid, ty, val, desc)
    if not valid:
        raise gen.Return({'ret': -1})

    # add into mine.balance
    tnow = int(time.time())
    col_mine = get_col_mine_mine()
    # insert if not exists
    doc = yield motordb.mongo_find_one_and_update(col_mine, {'_id': mid}, {'$inc': {'balance': val}, '$set': {'ut': tnow}}, upsert=True)
    if not doc:
        raise gen.Return({'ret': -1, 'data': {'msg': '服务器忙，请稍后再试吧~'}})

    balance = doc.get('balance', 0)
    raise gen.Return({'ret': 1, 'data': {'balance': balance}})


@gen.coroutine
def dync_bonus(mid, ty):
    mid = int(mid)
    if ty not in [BL_TYPE_DOWNLOAD_APP, BL_TYPE_VIEW_NEWS]:
        raise gen.Return({'ret': -1, 'data': {'msg': '不能识别的奖励类型'}})

    # check whether get this bonus in 24 hours
    col_mine = get_col_mine_mine()
    doc = yield motordb.mongo_find_one(col_mine, {'_id': mid})
    if not doc:
        raise gen.Return({'ret': -1, 'data': {'msg': '账户不存在'}})

    _bonus = doc.get('dync_bonus')
    if _bonus:
        ty_info = _bonus.get(str(ty))
        ntime = ty_info
