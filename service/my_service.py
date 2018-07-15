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

@gen.coroutine
def account_hello(phone):
    raise gen.Return({'ret':1, 'ph': phone})


@gen.coroutine
def download_history(mid, offset):
    col = get_col_action_down_hist()
    doc_list = yield motordb.mongo_find_sort_skip_limit(col, {'mid': mid}, [('ct', -1)], offset, HIST_PAGE + 1)

    if doc_list is False:
        raise gen.Return({'ret':-1, 'data': {'msg': '服务器忙，请稍后再试吧~'}})

    more = 1

    if len(doc_list) <= HIST_PAGE:
        more = 0
    else:
        doc_list = doc_list[0: HIST_PAGE]

    raise gen.Return({'ret': 1, 'data': {'more': more, 'list': doc_list, 'count': len(doc_list)}})


@gen.coroutine
def user_info(mid):
    mid = int(mid)
    col_member = get_col_account_member()
    doc = yield motordb.mongo_find_one(col_member, {'_id': mid})
    if not doc:
        raise gen.Return({'ret': -1011, 'data': {'msg': "未找到用户信息!"}})

    name = doc.get('name', '')

    col_mine = get_col_mine_mine()
    doc = yield motordb.mongo_find_one(col_mine, {'_id': mid})
    if doc is False:
        log.error('my.user_info@query col_produce, mid:%s' % mid)
        raise gen.Return({'ret': -1, 'data': {'msg': '服务器忙，请稍后再试吧~'}})

    power = doc.get('power', 0)
    balance = doc.get('balance', 0)

    raise gen.Return({'ret': 1, 'data': {'name': name, 'power': power, 'balance': balance,
                                         'url_white_paper': 'http://www.baidu.com'}})
