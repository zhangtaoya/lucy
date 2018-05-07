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


PR_COIN_PER_POWER_PER_HOUR = 0.5
PR_HOUR_FOR_RIPE = 8
PR_HOUR_FOR_LOST = 24

PR_STATUS_MINING = 1
PR_STATUS_MINE_LOST = 2


@gen.coroutine
def start_mine(mid):
    mid = int(mid)

    # S1. check whether already started
    col_produce = get_col_mine_produce()
    doc = yield motordb.mongo_find_one(col_produce, {'_id': mid})
    if doc is False:
        log.error('produce.start_mine@query col_produce, mid:%s' % mid)
        raise gen.Return({'ret': -1, 'data': {'msg': '服务器忙，请稍后再试吧~'}})
    if doc:
        t_ripe = int(doc.get('t_ripe', 0))
        t_left = int(time.time()) - t_ripe
        if t_left > PR_HOUR_FOR_RIPE * 3600 or t_left < 0:
            t_left = PR_HOUR_FOR_RIPE * 3600

        raise gen.Return({'ret': -1, 'data': {'msg': '正在挖矿中...', 'status': PR_STATUS_MINING, 't_left': t_left}})

    # S2. get power
    col_mine = get_col_mine_mine()
    doc = yield motordb.mongo_find_one(col_mine, {'_id': mid})
    if doc is False:
        log.error('produce.start_mine@query col_mine, mid:%s' % mid)
        raise gen.Return({'ret': -1, 'data': {'msg': '服务器忙，请稍后再试吧~'}})
    if not doc:
        log.warn('produce.start_mine@not reg, mid:%s' % mid)
        raise gen.Return({'ret': -1, 'data': {'msg': '您还未注册~'}})
    power = doc.get('power', 0)

    # S3. calc val, t_ripe, t_end
    val = PR_COIN_PER_POWER_PER_HOUR * PR_HOUR_FOR_RIPE * power
    t_ripe = int(time.time()) + PR_HOUR_FOR_RIPE * 3600
    t_end = int(time.time()) + (PR_HOUR_FOR_RIPE + PR_HOUR_FOR_LOST) * 3600

    # S4. insert record into produce
    ret = yield motordb.mongo_insert_one(col_produce, {'_id': mid, 'val': val, 't_ripe': t_ripe, 't_end': t_end})
    if not ret:
        log.error('produce.start_mine@insert col_produce, mid:%s' % mid)
        raise gen.Return({'ret': -1, 'data': {'msg': '服务器忙，请稍后再试吧~'}})

    log.info('produce.start_mine@succeed. mid:%s, power:%s, val:%s, t_ripe:%s, t_end:%s' %
             (mid, power, val, t_ripe, t_end))

    # todo actionlog
    raise gen.Return({'ret': 1, 'data': {'coin': val, 't_ripe': PR_HOUR_FOR_RIPE * 3600}})


@gen.coroutine
def collect_coin(mid):
    mid = int(mid)

    # S1. check whether already started
    col_produce = get_col_mine_produce()
    doc = yield motordb.mongo_find_one(col_produce, {'_id': mid})
    if doc is False:
        log.error('produce.collect_coin@query col_produce, mid:%s' % mid)
        raise gen.Return({'ret': -1, 'data': {'msg': '服务器忙，请稍后再试吧~'}})
    if not doc:
        raise gen.Return({'ret': -1, 'data': {'msg': '还未开始挖矿'}})

    # S2. check whether expired
    t_now = int(time.time())
    t_end = doc.get('t_end', 0)
    if t_now > t_end:
        yield motordb.mongo_delete_one(col_produce, {'_id': mid})
        raise gen.Return({'ret': -1, 'data': {'msg': '您的矿已流失', 'status': PR_STATUS_MINE_LOST}})

    # S3. check whether ripe
    t_ripe = doc.get('t_ripe', 0)
    if t_now < t_ripe:
        t_left = int(time.time()) - t_ripe
        if t_left > PR_HOUR_FOR_RIPE * 3600 or t_left < 0:
            t_left = PR_HOUR_FOR_RIPE * 3600
        raise gen.Return({'ret': -1, 'data': {'msg': '正在挖矿中...', 'status': PR_STATUS_MINING, 't_left': t_left}})

    # S4. get the riped coin, and delete the record
    val = doc.get('val', 0)
    ret = yield motordb.mongo_delete_one(col_produce, {'_id': mid})
    if not ret:
        log.error('produce.collect_coin@delete ripe recode col_produce, mid:%s, val:%s' % (mid, val))
        raise gen.Return({'ret': -1, 'data': {'msg': '服务器忙，请稍后再试吧~'}})

    log.info('produce.collect_coin@succeed. for rec:' % ujson.dumps(doc, ensure_ascii=False))
    raise gen.Return({'ret': 1, 'data': {'coin': val}})
