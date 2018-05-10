# -*- coding:utf-8 -*-
import ujson
from tornado import gen
from base_handler import BaseHandler
from service import mine_service
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
