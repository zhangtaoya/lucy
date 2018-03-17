import ujson
from tornado import gen
from base_handler import BaseHandler
from service import app_service
import log


class AppAddHandler(BaseHandler):
    _label = 'AddAppHandler'

    @gen.coroutine
    def post(self):
        log.debug('%s params:%s' % (self._label, ujson.dumps(self.params)))
        app = {
        'name': self.params.get('name', ''),
        'ver': self.params.get('ver', ''),
        'desc': self.params.get('desc', ''),
        'icon': self.params.get('icon', ''),
        'url': self.params.get('url', ''),
        'size': int(self.params.get('size', 1024*1024*1.7)),
        'rate': float(self.params.get('rate', 0)),
        'down_time': int(self.params.get('down_time', 0)),
        'down_user': int(self.params.get('down_user', 0)),
        'rec_rank': int(self.params.get('rec_rank', 0)),
        'hot_rank': int(self.params.get('hot_rank', 0)),
        'block_rank': int(self.params.get('block_rank', 0)),
        'new_rank': int(self.params.get('new_rank', 0))
        }

        ret = yield app_service.add(app)
        self.jsonify(ret)

class AppViewHandler(BaseHandler):
    _label = 'AddAppHandler'

    @gen.coroutine
    def post(self):
        log.debug('%s params:%s' % (self._label, ujson.dumps(self.params)))
        ts = int(self.params.get('ts', 0))
        mid = int(self.params.get('mid', 0))
        offset = int(self.params.get('offset', 0))
        ty = self.params.get('type', '')
        ret = yield app_service.view(mid, ty, offset)
        self.jsonify(ret)
 
