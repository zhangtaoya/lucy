import ujson
from tornado import gen
from base_handler import BaseHandler
import log

from service import account_service


class AccountPhone_verifyHandler(BaseHandler):
    _label = 'HelloHandler'

    @gen.coroutine
    def post(self):
        log.debug('%s params:%s' % (self._label, ujson.dumps(self.params)))
        phone = self.params.get('phone', '')
        ret = yield account_service.add_phone(phone)
        self.jsonify(ret)



class AccountRegHandler(BaseHandler):
    _label = 'HelloHandler'

    @gen.coroutine
    def post(self):
        log.debug('%s params:%s' % (self._label, ujson.dumps(self.params)))
        self.jsonify({'ret': 1, 'data': {'msg': 'hello'}})


class AccountPasswdHandler(BaseHandler):
    _label = 'HelloHandler'

    @gen.coroutine
    def post(self):
        log.debug('%s params:%s' % (self._label, ujson.dumps(self.params)))
        self.jsonify({'ret': 1, 'data': {'msg': 'hello'}})


class AccountLoginHandler(BaseHandler):
    _label = 'HelloHandler'

    @gen.coroutine
    def post(self):
        log.debug('%s params:%s' % (self._label, ujson.dumps(self.params)))
        self.jsonify({'ret': 1, 'data': {'msg': 'hello'}})


class AccountLogoutHandler(BaseHandler):
    _label = 'HelloHandler'

    @gen.coroutine
    def post(self):
        log.debug('%s params:%s' % (self._label, ujson.dumps(self.params)))
        self.jsonify({'ret': 1, 'data': {'msg': 'hello'}})