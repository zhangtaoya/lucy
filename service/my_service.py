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

    raise gen.Return({'ret':1, 'data': {'more': more, 'list': doc_list, 'count': len(doc_list)}})


