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

APP_PAGE = 20

@gen.coroutine
def account_hello(phone):
    raise gen.Return({'ret':1, 'ph': phone})


@gen.coroutine
def gen_appid():
    col = get_col_app_appid()
    id_name = 'appid'
    ret = yield motordb.mongo_find_one_and_update(col, {'_id': 'id'}, {'$inc': {id_name: 1}}, upsert=True, return_document=True)
    if not ret:
        raise gen.Return(-1)

    _id = ret.get(id_name)
    if _id:
        _id = int(_id)
    raise gen.Return(_id)


@gen.coroutine
def add(app):
    col = get_col_app_info()
    doc = yield motordb.mongo_find_one(col, {'name': app['name']})
    if doc:
        raise gen.Return({'ret':-2001, 'data': {'msg': '此app已入库'}})

    appid = yield gen_appid()
    if not appid:
        raise gen.Return({'ret':-2002, 'data': {'msg': '服务器忙，请稍后再试吧~'}})

    app['_id'] = appid
    app['ct'] = int(time.time())
    ret = yield motordb.mongo_insert_one(col, app)

    if not ret:
        raise gen.Return({'ret':-2003, 'data': {'msg': '添加app失败', 'app': app}})

    raise gen.Return({'ret':1, 'data': {'msg': '添加成功'}})


@gen.coroutine
def view(mid, ty, offset):
    ty_list = ['rec_rank', 'hot_rank', 'block_rank', 'new_rank']
    if ty not in ty_list:
        ty = 'rec_rank'

    col = get_col_app_info()
    doc_list = yield motordb.mongo_find_sort_skip_limit(col, {}, [(ty, -1)], offset, APP_PAGE + 1)
    if doc_list is False:
        raise gen.Return({'ret':-1, 'data': {'msg': '服务器忙，请稍后再试吧~'}})

    more = 1

    if len(doc_list) <= APP_PAGE:
        more = 0
    else:
        doc_list = doc_list[0: APP_PAGE]

    raise gen.Return({'ret':1, 'data': {'more': more, 'list': doc_list, 'count': len(doc_list)}})


@gen.coroutine
def download(mid, appid, ver):
    col_info = get_col_app_info()
    doc = yield motordb.mongo_find_one(col_info, {'_id': appid})
    if doc is False:
        raise gen.Return({'ret':-1, 'data': {'msg': '服务器忙，请稍后再试吧~'}})
    if not doc:
        raise gen.Return({'ret':-2011, 'data': {'msg': '此app已经下架'}})
    yield motordb.mongo_update_one(col_info, {'_id': appid}, {'$inc': {'down_time': 1}})
    app_name = doc.get('name')
    url = doc.get('url')

    col = get_col_action_down_hist()
    doc = yield motordb.mongo_find_one(col, {'mid': mid, 'appid': appid, 'ver': ver})
    if doc:
        raise gen.Return({'ret':1, 'data':{'msg': '已经下载此版本'}})

    ret = yield motordb.mongo_insert_one(col, {'mid': mid, 'appid': appid, 'ver': ver, 'name': app_name, 'url': url, 'ct': int(time.time())})
    if not ret:
        raise gen.Return({'ret':-2012, 'data': {'msg': '服务器忙，请稍后再试吧~'}})

    # charge
    ret_charge = 1
    if not ret_charge:
        ret = yield motordb.mongo_remove_one(col, {'mid': mid, 'appid': appid, 'ver': ver})
        if not ret:
            raise gen.Return({'ret':-2013, 'data': {'msg': '服务器忙，请稍后再试吧~'}})
        
    yield motordb.mongo_update_one(col_info, {'_id': appid}, {'$inc': {'down_user': 1}})
    raise gen.Return({'ret':1})
