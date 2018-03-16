import ujson
from tornado import gen
from base_handler import BaseHandler
from service import appstore_service
import log


class AddAppHandler(BaseHandler):
    _label = 'AddAppHandler'

    @gen.coroutine
    def post(self):
        log.debug('%s params:%s' % (self._label, ujson.dumps(self.params)))
        app = {
        '_id': self.params.get('name', ''),
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

        ret = yield appstore_service.add_app(app)
        self.jsonify(ret)
