# -*- coding:utf-8 -*-
import ujson
from tornado import gen
from base_handler import BaseHandler
from service import mine_service
from service import balance
from service import account_service
import log


class MineInfoHandler(BaseHandler):
    @gen.coroutine
    def post(self):
        log.debug('%s params:%s' % (self.__class__.__name__, ujson.dumps(self.params)))
        mid = int(self.params.get('mid', 0))
        phone = int(self.params.get('phone', 0))
        if not mid and not phone:
            self.jsonify({'ret': -1, 'data': {'msg': "数据错误"}})
            return
        if not mid:
            ret = yield account_service.get_mid_by_phone(phone)
            if ret.get('ret') != 1:
                self.jsonify({'ret': -1, 'data': {'msg': "账号未注册"}})
                return
            mid = ret['data']['mid']
        ret = yield mine_service.info(mid)
        self.jsonify(ret)


class MineCollectHandler(BaseHandler):
    @gen.coroutine
    def post(self):
        log.debug('%s params:%s' % (self.__class__.__name__, ujson.dumps(self.params)))
        mid = int(self.params.get('mid', 0))
        phone = int(self.params.get('phone', 0))
        if not mid and not phone:
            self.jsonify({'ret': -1, 'data': {'msg': "数据错误"}})
            return
        if not mid:
            ret = yield account_service.get_mid_by_phone(phone)
            if ret.get('ret') != 1:
                self.jsonify({'ret': -1, 'data': {'msg': "账号未注册"}})
                return
            mid = ret['data']['mid']
        ret = yield mine_service.collect_coin(mid)
        self.jsonify(ret)


class MineAddrVerifyHandler(BaseHandler):
    @gen.coroutine
    def post(self):
        log.debug('%s params:%s' % (self.__class__.__name__, ujson.dumps(self.params)))
        mid = int(self.params.get('mid', 0))
        ret = yield account_service.get_phone_by_mid(mid)
        if ret.get('ret') != 1:
            self.jsonify({'ret': -1, 'data': {'msg': "账号未注册"}})
            return
        phone = ret['data']['phone']
        ret = yield account_service.addr_verify(phone)
        self.jsonify(ret)


class MineAddrResetHandler(BaseHandler):
    @gen.coroutine
    def post(self):
        log.debug('%s params:%s' % (self.__class__.__name__, ujson.dumps(self.params)))
        mid = int(self.params.get('mid', 0))
        verify_code_md5 = self.params.get('verify_code', '')
        addr = self.params.get('addr', '')
        if not mid or not verify_code_md5 or not addr:
            self.jsonify({'ret': -1, 'data': {'msg': "数据错误"}})
            return

        ret = yield account_service.get_phone_by_mid(mid)
        if ret.get('ret') != 1:
            self.jsonify({'ret': -1, 'data': {'msg': "账号未注册"}})
            return
        phone = ret['data']['phone']
        ret = yield account_service.addr_reset(mid, phone, addr, verify_code_md5)
        self.jsonify(ret)


class MineWithdrawHandler(BaseHandler):
    @gen.coroutine
    def post(self):
        log.debug('%s params:%s' % (self.__class__.__name__, ujson.dumps(self.params)))
        mid = int(self.params.get('mid', 0))
        num = self.params.get('num', 0)
        if not mid or not num:
            self.jsonify({'ret': -1, 'data': {'msg': "数据错误"}})
            return
        self.jsonify({'ret': -1, 'data': {'msg': "提现成功，链上操作未对接暂未扣币"}})


class MineBonusHandler(BaseHandler):
    @gen.coroutine
    def post(self):
        log.debug('%s params:%s' % (self.__class__.__name__, ujson.dumps(self.params)))
        mid = int(self.params.get('mid', 0))
        ty = self.params.get('type', 0)
        if not mid or not ty:
            self.jsonify({'ret': -1, 'data': {'msg': "数据错误"}})
            return
        ret = yield balance.dync_bonus(mid, ty)
        self.jsonify(ret)
