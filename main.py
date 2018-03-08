# coding=utf-8
from tornado import ioloop, web
from tornado.options import define, parse_command_line, options
from tornado import gen
from datetime import datetime
import ujson
import traceback
import log
import sys
reload(sys)
sys.setdefaultencoding('utf8')
define('port', default=9000, type=int)

class MyApplication(web.Application):
    def __init__(
            self, handlers=None,
            default_host="",
            transforms=None,
            **settings
    ):
        web.Application.__init__(
            self, handlers,
            transforms,
            default_host,
            **settings
        )

class BaseHandler(web.RequestHandler):
    _label = 'BaseHandler'

    def __init__(self, application, request, **kwargs):
        web.RequestHandler.__init__(self, application, request, **kwargs)
        self.user_agent = None
        self.params = None
        self.test_mode = 0

    def head(self, *args, **kwargs):
        self.write('OK')
        self.finish()

    def prepare(self):
        if 'User-Agent' in self.request.headers:
            self.user_agent = self.request.headers['User-Agent'].lower()
        if self.request.body:
            self.params = ujson.loads(self.request.body)

    def on_finish(self):
        pass

    def jsonify(self, response):
        self.set_header('Cache-Control', 'private')
        self.set_header('Date', datetime.now())
        self.set_header('Access-Control-Allow-Origin', '*')

        response = ujson.dumps(response)
        self.set_header('Content-Type', 'application/json; charset=utf-8')
        self.write(response)
        self.finish()

    def write_error(self, status_code, **kwargs):
        """Override to implement custom error pages.

        ``write_error`` may call `write`, `render`, `set_header`, etc
        to produce output as usual.

        If this error was caused by an uncaught exception (including
        HTTPError), an ``exc_info`` triple will be available as
        ``kwargs["exc_info"]``.  Note that this exception may not be
        the "current" exception for purposes of methods like
        ``sys.exc_info()`` or ``traceback.format_exc``.
        """

        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            self.set_header('Content-Type', 'text/plain')
            for line in traceback.format_exception(*kwargs["exc_info"]):
                self.write(line)
            self.finish()
        else:
            if "exc_info" in kwargs and status_code >= 500:
                msg = "".join(traceback.format_exception(*kwargs.get("exc_info")))
                msg += "uri:%s\nbody:%s\nfrom:xcspam" % (self.request.uri, self.params)
                async_call_dingding(config.url_dingding_alarm_notify, msg)

            self.finish("<html><title>%(code)d: %(message)s</title>"
                        "<body>%(code)d: %(message)s</body></html>" % {
                            "code": status_code,
                            "message": self._reason,
                        })


class HelloHandler(BaseHandler):
    """
    """
    name='Hello'
    @gen.coroutine
    def post(self):
        """
        path: /hello
        :return: 
            ret 1 成功
            data 返回结果
                msg: hello
        """
        self.jsonify({'ret': 1, 'data': {"msg": 'hello'}})
 
def main():

    parse_command_line()

    app = MyApplication(
        [
            web.url(r'/hello', HelloHandler, name=HelloHandler.name),

        ],
        #debug=config.WEB_DEBUG,
        template_path='./template',
        static_path='./static',
    )

    log.info('zuiyou web listen on %d' % options.port)

    app.listen(options.port, xheaders=True)
    ioloop.IOLoop.instance().start()


if __name__ == '__main__':

    main()

