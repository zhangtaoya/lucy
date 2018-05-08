# -*- coding:utf-8 -*-
import ujson
from tornado import gen
from base_handler import BaseHandler
import log

from service import account_service
from service import mine_service


class AccountReg_verifyHandler(BaseHandler):
    _label = 'HelloHandler'

    @gen.coroutine
    def post(self):
        log.debug('%s params:%s' % (self._label, ujson.dumps(self.params)))
        phone = self.params.get('phone', '')
        if str(phone).isdigit() is False:
            self.jsonify({'ret': -1, 'data': {'msg': '手机号格式不正确'}})
            return
        phone = int(phone)
        if phone > 19012341234 or phone < 11012341234:
            self.jsonify({'ret': -1, 'data': {'msg': '目前仅对中国大陆地区用户开发注册'}})
            return
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
            return

        ret = yield account_service.reg(phone, verify_code_md5, passwd_encry)
        if ret.get('ret') != 1:
            self.jsonify(ret)
            return

        # login
        mid = ret.get('data').get('mid')
        passwd_md5 = ret.get('data').get('passwd')
        ret = yield account_service.login(mid, passwd_md5)
        if ret.get('ret') != 1:
            self.jsonify(ret)
            return
        ret['data']['mid'] = mid

        mine_service.reg_bonus(mid)
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
            return

        ret = yield account_service.passwd(phone, verify_code_md5, passwd_encry)
        if ret.get('ret') != 1:
            self.jsonify(ret)
            return

        # login
        mid = ret.get('data').get('mid')
        passwd_md5 = ret.get('data').get('passwd')
        ret = yield account_service.login(mid, passwd_md5)
        if ret.get('ret') != 1:
            self.jsonify(ret)
            return

        self.jsonify(ret)


class AccountLoginHandler(BaseHandler):
    _label = 'HelloHandler'

    @gen.coroutine
    def post(self):
        log.debug('%s params:%s' % (self._label, ujson.dumps(self.params)))
        mid = int(self.params.get('mid', 0))
        ts = int(self.params.get('ts', 0))
        passwd_md5 = self.params.get('passwd', '')
        sign = self.params.get('sign', '')
        if not mid or not ts or not sign:
            self.jsonify({'ret': -1, 'data':{'msg': "网络数据错误！请稍后再试"}})
            return

        ret = yield account_service.login(mid, passwd_md5)
        mine_service.login_bonus(mid)
        self.jsonify(ret)


class AccountLoginPhoneHandler(BaseHandler):
    _label = 'HelloHandler'

    @gen.coroutine
    def post(self):
        log.debug('%s params:%s' % (self._label, ujson.dumps(self.params)))
        phone = self.params.get('phone', 0)
        ts = int(self.params.get('ts', 0))
        passwd_md5 = self.params.get('passwd', '')
        sign = self.params.get('sign', '')
        if not phone or not ts or not sign:
            self.jsonify({'ret': -1, 'data':{'msg': "网络数据错误！请稍后再试"}})
            return

        ret = yield account_service.get_mid_by_phone(phone)
        if ret.get('ret') != 1:
            self.jsonify(ret)
            return

        ret = yield account_service.login(ret['data']['mid'], passwd_md5)
        self.jsonify(ret)



class AccountLogoutHandler(BaseHandler):
    _label = 'HelloHandler'

    @gen.coroutine
    def post(self):
        log.debug('%s params:%s' % (self._label, ujson.dumps(self.params)))
        mid = int(self.params.get('mid', 0))
        ts = int(self.params.get('ts', 0))
        passwd_md5 = self.params.get('passwd', '')
        sign = self.params.get('sign', '')
        if not mid or not ts or not sign:
            self.jsonify({'ret': -1, 'data':{'msg': "网络数据错误！请稍后再试"}})
            return

        ret = yield account_service.logout(mid, passwd_md5)
        self.jsonify(ret)

