# -*- coding:utf-8 -*-
import ujson
from tornado import gen
from base_handler import BaseHandler
from service import mine_service
import log


class MineInfoHandler(BaseHandler):
    _label = 'HelloHandler'

    @gen.coroutine
    def post(self):
        log.debug('%s params:%s' % (self._label, ujson.dumps(self.params)))
        mid = int(self.params.get('mid', 0))
        ret = yield mine_service.info(mid)
        self.jsonify(ret)


class MineStartHandler(BaseHandler):
    _label = 'HelloHandler'

    @gen.coroutine
    def post(self):
        log.debug('%s params:%s' % (self._label, ujson.dumps(self.params)))
        mid = int(self.params.get('mid', 0))
        ret = yield mine_service.start_mine(mid)
        self.jsonify(ret)


class MineCollectHandler(BaseHandler):
    _label = 'HelloHandler'

    @gen.coroutine
    def post(self):
        log.debug('%s params:%s' % (self._label, ujson.dumps(self.params)))
        mid = int(self.params.get('mid', 0))
        ret = yield mine_service.collect_coin(mid)
        self.jsonify(ret)
