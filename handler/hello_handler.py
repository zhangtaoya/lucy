import ujson
from tornado import gen
from base_handler import BaseHandler
import log

class HelloHandler(BaseHandler):
    _label = 'HelloHandler'

    @gen.coroutine
    def post(self):
        log.debug('%s params:%s' % (self._label, ujson.dumps(self.params)))
        self.jsonify({'ret':1, 'data':{'msg':'hello'}})

