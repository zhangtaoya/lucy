# -*- coding:utf-8 -*-
import ujson
from tornado import gen
from base_handler import BaseHandler
from service import mine_service
import log


class MineInfoHandler(BaseHandler):
    @gen.coroutine
    def post(self):
        log.debug('%s params:%s' % (self.__class__.__name__, ujson.dumps(self.params)))
        mid = int(self.params.get('mid', 0))
        ret = yield mine_service.info(mid)
        self.jsonify(ret)


class MineCollectHandler(BaseHandler):
    @gen.coroutine
    def post(self):
        log.debug('%s params:%s' % (self.__class__.__name__, ujson.dumps(self.params)))
        mid = int(self.params.get('mid', 0))
        ret = yield mine_service.collect_coin(mid)
        self.jsonify(ret)
