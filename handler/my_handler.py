# -*- coding:utf-8 -*-
import ujson
from tornado import gen
from base_handler import BaseHandler
from service import my_service
import log


class MyDownloadHistoryHandler(BaseHandler):
    @gen.coroutine
    def post(self):
        log.debug('%s params:%s' % (self.__class__.__name__, ujson.dumps(self.params)))
        mid = int(self.params.get('mid', 0))
        offset = int(self.params.get('offset', 0))
        ret = yield my_service.download_history(mid, offset)
        self.jsonify(ret)

