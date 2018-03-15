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
import uuid
import time
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

@gen.coroutine
def account_hello(phone):
    raise gen.Return({'ret':1, 'ph': phone})

def phone_verifycode_cache_key(phone):
    return str(phone) + "_verify"


def get_cached_verifycode(phone):
    cache_key = phone_verifycode_cache_key(phone)
    cache = get_redis()
    verify_code = cache.get(cache_key)
    return verify_code


def get_md5(src):
    m = md5.new()
    m.update(src)
    return m.hexdigest()


def lucy_decry(key, passwd_encry):
    return passwd_encry.replace(key, '')


def lucy_sign(key, txt):
    src = str(key) + ',' + txt
    return get_md5(src)


@gen.coroutine
def gen_mid():
    col = get_col_account_mid()
    ret = yield motordb.mongo_find_one_and_update(col, {'_id': 'id'}, {'$inc': {'mid': 1}}, upsert=True, return_document=True)
    if not ret:
        raise gen.Return(-1)

    mid = ret.get('mid')
    if mid:
        mid = int(mid)
    raise gen.Return(mid)


@gen.coroutine
def send_verify_code(phone):
    # call
    #  resp = yield call.async_post(config.url_phone_verify_code, {'phone': phone}, retjson=False)
    verify_code = '123433'
    raise gen.Return(verify_code)


@gen.coroutine
def reg_verify(phone):
    phone = int(phone)
    phone_str = str(phone)
    col = get_col_account_member()
    doc = yield motordb.mongo_find_one(col, {'phone': phone})
    if doc is False:
        log.error("db failed")
        raise gen.Return({'ret': -1001, 'data': {'msg': "服务器正忙，请稍后再试吧"}})

    if doc:
        raise gen.Return({'ret': -1002, 'data': {'msg': "此手机号已经注册"}})

    verify_key = get_cached_verifycode(phone)
    if verify_key:
        raise gen.Return({'ret': -1003, 'data': {'msg': "此手机号已经获取了验证码，请稍后再获取吧"}})

    verify_code = yield send_verify_code(phone)

    cache = get_redis()
    cache_key = phone_verifycode_cache_key(phone)
    cache.set(cache_key, verify_code)
    cache.expire(cache_key, 162)
    raise gen.Return({'ret': 1, 'data': {'code': verify_code}})


@gen.coroutine
def reg(phone, verify_code_app_md5, passwd_encry):
    col = get_col_account_member()
    doc = yield motordb.mongo_find_one(col, {'phone': phone})
    if doc:
        log.error("db failed")
        raise gen.Return({'ret': -1012, 'data': {'msg': "该手机号已经注册!"}})

    verify_code_srv = get_cached_verifycode(phone)
    if not verify_code_srv:
        raise gen.Return({'ret':-1011, 'data': {'msg': '验证码已经过期，请重新获取验证码。'}})

    verify_code_srv_md5 = get_md5(verify_code_srv)
    if verify_code_srv_md5 != verify_code_app_md5:
        raise gen.Return({'ret':-1012, 'data': {'msg': '验证码不正确，请重新输入验证码。'}})

    passwd = lucy_decry(verify_code_srv, passwd_encry)
    mid = yield gen_mid()
    if not mid:
        log.error("gen mid failed")
        raise gen.Return({'ret': -1001, 'data': {'msg': "服务器正忙，请稍后再试吧"}})

    ret = yield motordb.mongo_insert_one(col, {'_id': mid, 'phone': phone, 'passwd': passwd})

    raise gen.Return({'ret':1, 'data': {'mid': mid}})


@gen.coroutine
def passwd_verify(phone):
    phone = int(phone)
    phone_str = str(phone)
    col = get_col_account_member()
    doc = yield motordb.mongo_find_one(col, {'phone': phone})
    if doc is False:
        log.error("db failed")
        raise gen.Return({'ret': -1001, 'data': {'msg': "服务器正忙，请稍后再试吧"}})

    if not doc:
        raise gen.Return({'ret': -1002, 'data': {'msg': "此手机号未注册"}})

    verify_key = get_cached_verifycode(phone)
    if verify_key:
        raise gen.Return({'ret': -1003, 'data': {'msg': "此手机号已经获取了验证码，请稍后再获取吧"}})

    

    verify_code = yield send_verify_code(phone)

    cache = get_redis()
    cache_key = phone_verifycode_cache_key(phone)
    cache.set(cache_key, verify_code)
    cache.expire(cache_key, 162)
    raise gen.Return({'ret': 1, 'data': {'code': verify_code}})


@gen.coroutine
def passwd(phone, verify_code_app_md5, passwd_encry):
    col = get_col_account_member()
    doc = yield motordb.mongo_find_one(col, {'phone': phone})
    if not doc:
        raise gen.Return({'ret': -1021, 'data': {'msg': "未查到该用户!"}})

    verify_code_srv = get_cached_verifycode(phone)
    if not verify_code_srv:
        raise gen.Return({'ret':-1023, 'data': {'msg': '验证码已经过期，请重新获取验证码。'}})

    verify_code_srv_md5 = get_md5(verify_code_srv)
    if verify_code_srv_md5 != verify_code_app_md5:
        raise gen.Return({'ret':-1024, 'data': {'msg': '验证码不正确，请重新输入验证码。'}})

    passwd = lucy_decry(verify_code_srv, passwd_encry)
    ret = yield motordb.mongo_update_one(col, {'phone': phone}, {'$set': {'passwd': passwd}})

    raise gen.Return({'ret':1})


@gen.coroutine
def account_service.login(mid, ts, sign_app):
    col = get_col_account_member()
    doc = yield motordb.mongo_find_one(col, {'mid': mid})
    if doc is False:
        log.error("db failed")
        raise gen.Return({'ret': -1001, 'data': {'msg': "服务器正忙，请稍后再试吧"}})
    if not doc:
        raise gen.Return({'ret': -1021, 'data': {'msg': "未查到该用户!"}})
    
    passwd = doc.get('passwd')
    sign_srv = lucy_sign(passwd, ','.join([str(mid), str(ts), str(1)]))
    if sign_srv != sign_app:
