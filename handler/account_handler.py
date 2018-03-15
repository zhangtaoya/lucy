# -*- coding:utf-8 -*-
import ujson
from tornado import gen
from base_handler import BaseHandler
import log

from service import account_service


class AccountReg_verifyHandler(BaseHandler):
    _label = 'HelloHandler'

    @gen.coroutine
    def post(self):
        log.debug('%s params:%s' % (self._label, ujson.dumps(self.params)))
        phone = self.params.get('phone', '')
        ret = yield account_service.reg_verify(phone)
        self.jsonify(ret)



class AccountRegHandler(BaseHandler):
    _label = 'HelloHandler'

    @gen.coroutine
    def post(self):
        log.debug('%s params:%s' % (self._label, ujson.dumps(self.params)))
        phone = int(self.params.get('phone', 0))
        verify_code_md5 = self.params.get('verify_code', '')
        passwd_encry = self.params.get('passwd', '')
        if not phone or not verify_code_md5 or not passwd_encry:
            self.jsonify({'ret': -1, 'data':{'msg': "网络数据错误！请稍后再试"}})

        ret = yield account_service.reg(phone, verify_code_md5, passwd_encry)
        self.jsonify(ret)

class AccountPasswd_verifyHandler(BaseHandler):
    _label = 'HelloHandler'

    @gen.coroutine
    def post(self):
        log.debug('%s params:%s' % (self._label, ujson.dumps(self.params)))
        phone = int(self.params.get('phone', 0))
        ret = yield account_service.passwd_verify(phone)
        self.jsonify(ret)


class AccountPasswdHandler(BaseHandler):
    _label = 'HelloHandler'

    @gen.coroutine
    def post(self):
        log.debug('%s params:%s' % (self._label, ujson.dumps(self.params)))
        phone = int(self.params.get('phone', 0))
        verify_code_md5 = self.params.get('verify_code', '')
        passwd_encry = self.params.get('passwd', '')
        if not phone or not verify_code_md5 or not passwd_encry:
            self.jsonify({'ret': -1, 'data':{'msg': "网络数据错误！请稍后再试"}})

        ret = yield account_service.passwd(phone, verify_code_md5, passwd_encry)
        self.jsonify(ret)


class AccountLoginHandler(BaseHandler):
    _label = 'HelloHandler'

    @gen.coroutine
    def post(self):
        log.debug('%s params:%s' % (self._label, ujson.dumps(self.params)))
        mid = int(self.params.get('mid', 0))
        ts = int(self.params.get('ts', 0))
        sign = self.params.get('sign', '')
        if not mid or not ts or not sign:
            self.jsonify({'ret': -1, 'data':{'msg': "网络数据错误！请稍后再试"}})

        ret = yield account_service.login(mid, ts, sign)
        self.jsonify(ret)


class AccountLogoutHandler(BaseHandler):
    _label = 'HelloHandler'

    @gen.coroutine
    def post(self):
        log.debug('%s params:%s' % (self._label, ujson.dumps(self.params)))
        self.jsonify({'ret': 1, 'data': {'msg': 'hello'}})
