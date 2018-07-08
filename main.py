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


def main():

    parse_command_line()
    from route import routes as handlers
    app = MyApplication(
        handlers,
        debug=True,
        template_path='./template',
        static_path='./static',
    )
    log.set_level(None, 'DEBUG')
    log.info('tangcity listen on %d' % options.port)

    app.listen(options.port, xheaders=True)
    ioloop.IOLoop.instance().start()


if __name__ == '__main__':

    main()

