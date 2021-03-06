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
import hashlib
import time
import random
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


TTL_VERIFY_CODE = 182
TTL_NONCE = 7 * 24 * 3600


@gen.coroutine
def account_hello(phone):
    raise gen.Return({'ret':1, 'ph': phone})


def phone_verifycode_cache_key(phone):
    return str(phone) + "_verify"


def mid_nonce_cache_key(mid):
    return str(mid) + "_nonce"


def phone_addrcode_cache_key(phone):
    return str(phone) + "_addr"


def get_cached_verifycode(phone):
    cache_key = phone_verifycode_cache_key(phone)
    cache = get_redis()
    verify_code = cache.get(cache_key)
    return verify_code


def get_cached_addrverifycode(phone):
    cache_key = phone_addrcode_cache_key(phone)
    cache = get_redis()
    verify_code = cache.get(cache_key)
    return verify_code


def get_md5(src):
    md5_str = hashlib.md5(str(src)).hexdigest()
    return md5_str


def lucy_decry(key, encry_txt):
    return encry_txt.replace(key, '')


def rand_str():
    n = random.randint(0, 1E12)
    return get_md5(n)


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
        raise gen.Return({'ret': -1, 'data': {'msg': "服务器正忙，请稍后再试吧"}})

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
    raise gen.Return({'ret': 1})
    #raise gen.Return({'ret': 1, 'data': {'code': verify_code}})


@gen.coroutine
def reg(phone, verify_code_app_md5, passwd_encry):
    col = get_col_account_member()
    doc = yield motordb.mongo_find_one(col, {'phone': phone})
    if doc:
        raise gen.Return({'ret': -1011, 'data': {'msg': "该手机号已经注册!"}})

    verify_code_srv = get_cached_verifycode(phone)
    if not verify_code_srv:
        raise gen.Return({'ret':-1012, 'data': {'msg': '验证码已经过期，请重新获取验证码。'}})

    verify_code_srv_md5 = get_md5(verify_code_srv)
    if verify_code_srv_md5 != verify_code_app_md5:
        raise gen.Return({'ret':-1013, 'data': {'msg': '验证码不正确，请重新输入验证码。'}})

    passwd = passwd_encry
    mid = yield gen_mid()
    if not mid:
        log.error("gen mid failed")
        raise gen.Return({'ret': -1, 'data': {'msg': "服务器正忙，请稍后再试吧"}})

    ret = yield motordb.mongo_insert_one(col, {'_id': mid, 'phone': phone, 'passwd': passwd, 'ct': int(time.time())})

    raise gen.Return({'ret':1, 'data': {'mid': mid, 'passwd': get_md5(passwd)}})


@gen.coroutine
def passwd_verify(phone):
    phone = int(phone)
    col = get_col_account_member()
    doc = yield motordb.mongo_find_one(col, {'phone': phone})
    if doc is False:
        log.error("db failed")
        raise gen.Return({'ret': -1, 'data': {'msg': "服务器正忙，请稍后再试吧"}})

    if not doc:
        raise gen.Return({'ret': -1021, 'data': {'msg': "此手机号未注册"}})

    verify_key = get_cached_verifycode(phone)
    if verify_key:
        raise gen.Return({'ret': -1022, 'data': {'msg': "此手机号已经获取了验证码，请稍后再获取吧"}})

    verify_code = yield send_verify_code(phone)

    cache = get_redis()
    cache_key = phone_verifycode_cache_key(phone)
    cache.set(cache_key, verify_code)
    cache.expire(cache_key, TTL_VERIFY_CODE)
    raise gen.Return({'ret': 1})


@gen.coroutine
def addr_verify(phone):
    phone = int(phone)
    col = get_col_account_member()
    doc = yield motordb.mongo_find_one(col, {'phone': phone})
    if doc is False:
        log.error("db failed")
        raise gen.Return({'ret': -1, 'data': {'msg': "服务器正忙，请稍后再试吧"}})

    if not doc:
        raise gen.Return({'ret': -1021, 'data': {'msg': "此手机号未注册"}})

    verify_code_srv = get_cached_addrverifycode(phone)
    if verify_code_srv:
        raise gen.Return({'ret': -1022, 'data': {'msg': "此手机号已经获取了验证码，请稍后再获取吧"}})

    verify_code = yield send_verify_code(phone)

    cache = get_redis()
    cache_key = phone_addrcode_cache_key(phone)
    cache.set(cache_key, verify_code)
    cache.expire(cache_key, TTL_VERIFY_CODE)
    raise gen.Return({'ret': 1})


@gen.coroutine
def addr_reset(mid, phone, addr, verify_code_app_md5):
    col = get_col_account_member()
    doc = yield motordb.mongo_find_one(col, {'phone': phone})
    if not doc:
        raise gen.Return({'ret': -1031, 'data': {'msg': "未查到该用户!"}})
    if mid != doc['_id']:
        raise gen.Return({'ret': -1031, 'data': {'msg': "用户资料错误!"}})

    verify_code_srv = get_cached_addrverifycode(phone)
    if not verify_code_srv:
        raise gen.Return({'ret':-1032, 'data': {'msg': '验证码已经过期，请重新获取验证码。'}})

    verify_code_srv_md5 = get_md5(verify_code_srv)
    if verify_code_srv_md5 != verify_code_app_md5:
        raise gen.Return({'ret':-1033, 'data': {'msg': '验证码不正确，请重新输入验证码。'}})

    ret = yield motordb.mongo_update_one(col, {'mid': mid}, {'$set': {'addr': addr}})
    if not ret:
        raise gen.Return({'ret': -1032, 'data': {'msg': '服务器忙，请稍后再试。'}})

    raise gen.Return({'ret':1})


@gen.coroutine
def passwd(phone, verify_code_app_md5, passwd_encry):
    col = get_col_account_member()
    doc = yield motordb.mongo_find_one(col, {'phone': phone})
    if not doc:
        raise gen.Return({'ret': -1031, 'data': {'msg': "未查到该用户!"}})

    mid = doc['_id']

    verify_code_srv = get_cached_verifycode(phone)
    if not verify_code_srv:
        raise gen.Return({'ret':-1032, 'data': {'msg': '验证码已经过期，请重新获取验证码。'}})

    verify_code_srv_md5 = get_md5(verify_code_srv)
    if verify_code_srv_md5 != verify_code_app_md5:
        raise gen.Return({'ret':-1033, 'data': {'msg': '验证码不正确，请重新输入验证码。'}})

    passwd = passwd_encry
    ret = yield motordb.mongo_update_one(col, {'phone': phone}, {'$set': {'passwd': passwd}})

    raise gen.Return({'ret':1, 'data':{'mid': mid, 'passwd': get_md5(passwd)}})


def verify_token(mid, token):
    key = mid_nonce_cache_key(mid)
    cache = get_redis()
    nonce = cache.get(key)
    if not nonce:
        return {'ret': -1052, 'data': {'msg': "用户状态异常，请重置登陆密码!"}}

    nonce_encry = get_md5(nonce)
    if nonce_encry != token:
        return {'ret': -1052, 'data': {'msg': "token错误!"}}
    return {'ret': 1}


@gen.coroutine
def login(mid, passwd_app_md5):
    col = get_col_account_member()
    doc = yield motordb.mongo_find_one(col, {'_id': mid})
    if doc is False:
        log.error("db failed")
        raise gen.Return({'ret': -1, 'data': {'msg': "服务器正忙，请稍后再试吧"}})
    if not doc:
        raise gen.Return({'ret': -1041, 'data': {'msg': "未查到该用户!"}})
    passwd = doc.get('passwd')
    if not passwd:
        raise gen.Return({'ret': -1042, 'data': {'msg': "用户状态异常，请重置登陆密码!"}})

    if get_md5(passwd) != passwd_app_md5:
        raise gen.Return({'ret': -1043, 'data': {'msg': "密码错误!"}})
        
    nonce = rand_str()
    key = mid_nonce_cache_key(mid)
    cache = get_redis()
    cache.set(key, nonce)
    cache.expire(key, TTL_NONCE)

    nonce_encry = get_md5(nonce)
    raise gen.Return({'ret': 1, 'data': {'nonce': nonce_encry, 'mid': mid}})


@gen.coroutine
def logout(mid, passwd_app_md5):
    col = get_col_account_member()
    doc = yield motordb.mongo_find_one(col, {'_id': mid})
    if doc is False:
        log.error("db failed")
        raise gen.Return({'ret': -1, 'data': {'msg': "服务器正忙，请稍后再试吧"}})
    if not doc:
        raise gen.Return({'ret': -1051, 'data': {'msg': "未查到该用户!"}})
    passwd = doc.get('passwd')
    if not passwd:
        raise gen.Return({'ret': -1052, 'data': {'msg': "用户状态异常，请重置登陆密码!"}})

    if get_md5(passwd) != passwd_app_md5:
        raise gen.Return({'ret': -1053, 'data': {'msg': "退出成功！"}})

    key = mid_nonce_cache_key(mid)
    cache = get_redis()
    cache.delete(key)
    raise gen.Return({'ret':1, 'data':{'msg': '退出成功！'}})


@gen.coroutine
def get_mid_by_phone(phone):
    if str(phone).isdigit() is False:
        raise gen.Return({'ret': -1, 'data': {'msg': '手机号码格式不对'}})

    phone = int(phone)
    col = get_col_account_member()
    doc = yield motordb.mongo_find_one(col, {'phone': phone})
    if not doc:
        raise gen.Return({'ret': -1, 'data': {'msg': '手机号码未注册'}})

    mid = int(doc['_id'])
    raise gen.Return({'ret': 1, 'data': {'mid': mid}})


@gen.coroutine
def get_phone_by_mid(mid):
    mid = int(mid)
    col = get_col_account_member()
    doc = yield motordb.mongo_find_one(col, {'_id': mid})
    if not doc:
        raise gen.Return({'ret': -1, 'data': {'msg': '手机号码未注册'}})

    phone = int(doc['phone'])
    raise gen.Return({'ret': 1, 'data': {'phone': phone}})


@gen.coroutine
def update(mid, name, avatar):
    upd = {'name': name}
    if avatar:
        upd = {'avatar': avatar}
    col = get_col_account_member()
    yield motordb.mongo_update_one(col, {'_id': mid}, {'$set': upd})
    raise gen.Return({'ret': 1})
