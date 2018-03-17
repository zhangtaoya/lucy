# -*- coding:utf-8 -*-
import ujson
from tornado import gen
from base_handler import BaseHandler
from service import my_service
import log


class HelloHandler(BaseHandler):
    _label = 'HelloHandler'

    @gen.coroutine
    def post(self):
        log.debug('%s params:%s' % (self._label, ujson.dumps(self.params)))
        ret = yield account_service.account_hello(1112)
        self.jsonify(ret)


class MyDownloadHistoryHandler(BaseHandler):
    _label = 'HelloHandler'

    @gen.coroutine
    def post(self):
        log.debug('%s params:%s' % (self._label, ujson.dumps(self.params)))
        mid = int(self.params.get('mid', 0))
        offset = int(self.params.get('offset', 0))
        ret = yield my_service.download_history(mid, offset)
        self.jsonify(ret)

