#!/usr/bin/env python
#coding:utf-8

import os.path
import time
from PIL import Image,ImageDraw,ImageFont

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

import sys
reload(sys)
sys.setdefaultencoding('utf8')


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class UserHandler(tornado.web.RequestHandler):
    def post(self):
        day_comment = self.get_argument("day_comment")
        title = self.get_argument("title")
        cont = self.get_argument("cont")
        #self.render("user.html",username=user_name,email=user_email,website=user_website,language=user_language)
        data = open('xx.jpg').read()
        self.write(data)
        self.set_header("Content-type", "image/jpeg")
    def get(self):
        self.render("index.html")

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        data = open('t.jpg').read()
        self.write(data)
        self.set_header("Content-type", "image/jpg")

def get_date_desc():
    # time.struct_time(tm_year=2018, tm_mon=4, tm_mday=1, tm_hour=20, tm_min=14, tm_sec=22, tm_wday=6, tm_yday=91, tm_isdst=0)
    to = time.localtime(time.time())
    wd = ["一","二","三","四","五","六","日"]
    str_day = "%d年%d月%d日 %02d:%02d:%02d 星期%s" % (to.tm_year, to.tm_mon, to.tm_mday, to.tm_hour, to.tm_min, to.tm_sec, wd[to.tm_wday])
    return str_day

def draw_lsj_img(file_name, day_comment, title, cont):
    font_day_comment = ImageFont.truetype("SourceHanSansCN-Regular.ttf",24)
    font_title = ImageFont.truetype("chuti.ttf",24)
    font_cont = ImageFont.truetype("putong.ttf",24)
    im = Image.open(file_name)
    draw = ImageDraw.Draw(im)
    str_day = get_date_desc() + " " + day_comment
    draw.text((80,335),str_day, fill=(0,0,0),font=font_day_comment)

    title_arr = title.strip().replace('\r', '\n').replace('\n\n', '\n').split('\n')
    hi = 0
    for title in title_arr:
        draw.text((55,387 + hi),title, fill=(100,0,0),font=font_title)
        draw.text((55,387 + hi),title, fill=(100,0,0),font=font_title)
        draw.text((55,387 + hi),title, fill=(100,0,0),font=font_title)
        hi += 50

    cont_arr = cont.strip().replace('\r', '\n').replace('\n\n', '\n').split('\n')
    hi = 0
    for cont in cont_arr:
        draw.text((55,387 + hi),cont, fill=(0,0,0),font=font_cont)
        hi += 50

    im.save("xx_lsj.jpg")
    return

class LSJHandler(tornado.web.RequestHandler):
    def post(self):
        day_comment = self.get_argument("day_comment")
        title = self.get_argument("title")
        cont = self.get_argument("cont")
        #self.render("user.html",username=user_name,email=user_email,website=user_website,language=user_language)
        draw_lsj_img("LSJ.jpg", day_comment, title, cont)
        data = open('xx_lsj.jpg').read()
        self.write(data)
        self.set_header("Content-type", "image/jpg")
    def get(self):
        self.render("index.html")

def draw_pai_img(file_name, day_comment, title, cont):
    font_title=font_cont=font_day_comment = ImageFont.truetype("SourceHanSansCN-Regular.ttf",35)
    #font_title = ImageFont.truetype("chuti.ttf",38)
    #font_cont = ImageFont.truetype("putong.ttf",38)
    im = Image.open(file_name)
    draw = ImageDraw.Draw(im)
    str_day = get_date_desc() + " " + day_comment
    draw.text((143,490),str_day, fill=(0,0,0),font=font_day_comment)

    title_arr = title.strip().replace('\r', '\n').replace('\n\n', '\n').split('\n')
    hi = 0
    dh = 65
    h0 = 587
    x0 = 65
    for title in title_arr:
        draw.text((x0, h0 + hi),title, fill=(100,0,0),font=font_title)
        draw.text((x0, h0 + hi),title, fill=(100,0,0),font=font_title)
        draw.text((x0, h0 + hi),title, fill=(100,0,0),font=font_title)
        hi += dh

    cont_arr = cont.strip().replace('\r', '\n').replace('\n\n', '\n').split('\n')
    hi = 0
    for cont in cont_arr:
        draw.text((x0,h0 + hi),cont, fill=(0,0,0),font=font_cont)
        hi += dh

    im.save("xx_pai.jpg")
    return


class PAIHandler(tornado.web.RequestHandler):
    def post(self):
        day_comment = self.get_argument("day_comment")
        title = self.get_argument("title")
        cont = self.get_argument("cont")
        #self.render("user.html",username=user_name,email=user_email,website=user_website,language=user_language)
        draw_pai_img("PAI.jpg", day_comment, title, cont)
        data = open('xx_pai.jpg').read()
        self.write(data)
        self.set_header("Content-type", "image/jpg")
    def get(self):
        self.render("index_pai.html")



handlers = [
    (r"/", IndexHandler),
    (r"/user", UserHandler),
    (r"/t", TestHandler),
    (r"/lsj", LSJHandler),
    (r"/pai", PAIHandler),
]

template_path = os.path.join(os.path.dirname(__file__),"template")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers, template_path)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
