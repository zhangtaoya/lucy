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
PR_STATUS_MINE_RIPE = 2
PR_STATUS_MINE_LOST = 3


@gen.coroutine
def refresh_mine(mid):
    mid = int(mid)

    col_mine = get_col_mine_mine()
    doc = yield motordb.mongo_find_one(col_mine, {'_id': mid})

    # S2. get power
    power = doc.get('power', 0)

    # S3. calc val, t_ripe, t_end
    val = PR_COIN_PER_POWER_PER_HOUR * PR_HOUR_FOR_RIPE * power
    t_ripe = int(time.time()) + PR_HOUR_FOR_RIPE * 3600
    t_end = int(time.time()) + (PR_HOUR_FOR_RIPE + PR_HOUR_FOR_LOST) * 3600

    # S4. insert record into produce
    ret = yield motordb.mongo_update_one(col_mine,
                                         {'_id': mid},
                                         {'$set': {'produce': {'val': val,
                                                               't_ripe': t_ripe,
                                                               't_end': t_end}
                                                   }
                                          })
    if not ret:
        log.error('produce.start_mine@insert col_produce, mid:%s' % mid)
        raise gen.Return({'ret': -1, 'data': {'msg': '服务器忙，请稍后再试吧~'}})

    log.info('produce.start_mine@succeed. mid:%s, power:%s, val:%s, t_ripe:%s, t_end:%s' %
             (mid, power, val, t_ripe, t_end))

    # todo actionlog
    raise gen.Return({'ret': 1, 'data': {'coin': val, 'status': PR_STATUS_MINING, 't_left': PR_HOUR_FOR_RIPE * 3600}})


@gen.coroutine
def collect_coin(mid):
    mid = int(mid)
    col_mine = get_col_mine_mine()
    doc = yield motordb.mongo_find_one(col_mine, {'_id': mid})
    # S0. check whether registered
    if doc is False:
        log.error('produce.collect_coin@query col_produce, mid:%s' % mid)
        raise gen.Return({'ret': -1, 'data': {'msg': '服务器忙，请稍后再试吧~'}})
    if not doc:
        log.warn('produce.collect_coin@not reg, mid:%s' % mid)
        raise gen.Return({'ret': -1, 'data': {'msg': '您还未注册~'}})

    produce = doc.get('produce')
    # S1. check whether already started
    if not produce:
        ret = yield refresh_mine(mid)
        raise gen.Return(ret)

    # S2. check whether expired
    t_now = int(time.time())
    t_end = produce.get('t_end', 0)
    if t_now > t_end:
        log.info('produce.collect_coin@mid:%s coin loss, detail:%s' % (mid, ujson.dumps(produce)))
        yield refresh_mine(mid)
        raise gen.Return({'ret': -1, 'data': {'msg': '您的矿已流失'}})

    # S3. check whether ripe
    t_ripe = produce.get('t_ripe', 0)
    if t_now < t_ripe:
        t_left = t_ripe - int(time.time())
        if t_left > PR_HOUR_FOR_RIPE * 3600 or t_left < 0:
            t_left = PR_HOUR_FOR_RIPE * 3600
        raise gen.Return({'ret': -1, 'data': {'msg': '正在挖矿中...', 'status': PR_STATUS_MINING, 't_left': t_left}})

    # S4. get the riped coin, and delete the record
    val = produce.get('val', 0)
    ret = yield motordb.mongo_update_one(col_mine, {'_id': mid}, {'$unset': {'produce': 1}})
    if not ret:
        log.error('produce.collect_coin@delete ripe recode col_produce, mid:%s, val:%s' % (mid, val))
        raise gen.Return({'ret': -1, 'data': {'msg': '服务器忙，请稍后再试吧~'}})

    log.info('produce.collect_coin@succeed. for mid:%s, produce:%s' % (mid, ujson.dumps(produce, ensure_ascii=False)))
    raise gen.Return({'ret': 1, 'data': {'coin': val}})


def build_produce_info(produce_info):
    t_ripe = produce_info['t_ripe']
    t_end = produce_info['t_end']
    ts_now = int(time.time())

    t_left = t_ripe - ts_now
    t_missing = t_end - ts_now

    produce_info['t_left'] = t_left
    if t_missing < 0:
        produce_info['status'] = PR_STATUS_MINE_LOST
    elif t_left < 0:
        produce_info['status'] = PR_STATUS_MINE_RIPE
    else:
        produce_info['status'] = PR_STATUS_MINING
