import ujson
from datetime import datetime
import traceback
from tornado import web


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

        response = ujson.dumps(response, ensure_ascii=False)
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
                #  error hook
                #  async_call_dingding(config.url_dingding_alarm_notify, msg)

            self.finish("<html><title>%(code)d: %(message)s</title>"
                        "<body>%(code)d: %(message)s</body></html>" % {
                            "code": status_code,
                            "message": self._reason,
                        })


