#!/usr/bin/env python
#coding:utf-8

import os.path
import time
import StringIO
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

def auto_align(cont, n_c):
    cont_strip = cont.strip().replace('\r', '\n').replace('\n\n', '\n')
    cont_arr = cont_strip.split('\n')
    #return cont_arr
    cont_arr = []

    n_ch = 0
    str_i = ''
    for c in cont_strip:
        if c == '\n':
            cont_arr.append(str_i)
            str_i = ''
            n_ch = 0
            continue

        str_i += c
        if 'A' <= c <= 'Z':
            n_ch += 1/1.3
        elif '!' <= c <= '~':
            n_ch += 1/2.1
        else:
            n_ch += 1
        if n_ch >= n_c:
            cont_arr.append(str_i)
            str_i = ''
            n_ch = n_en = 0

    if str_i:
        cont_arr.append(str_i)

    return cont_arr

def get_date_desc():
    # time.struct_time(tm_year=2018, tm_mon=4, tm_mday=1, tm_hour=20, tm_min=14, tm_sec=22, tm_wday=6, tm_yday=91, tm_isdst=0)
    to = time.localtime(time.time())
    wd = ["一","二","三","四","五","六","日"]
    str_day = "%d年%d月%d日 %02d:%02d:%02d 星期%s" % (to.tm_year, to.tm_mon, to.tm_mday, to.tm_hour, to.tm_min, to.tm_sec, wd[to.tm_wday])
    return str_day

def get_date_desc_baic():
    # time.struct_time(tm_year=2018, tm_mon=4, tm_mday=1, tm_hour=20, tm_min=14, tm_sec=22, tm_wday=6, tm_yday=91, tm_isdst=0)
    to = time.localtime(time.time())
    wd = ["一","二","三","四","五","六","日"]
    #str_day = "%d.%02d.%02d 星期%s" % (to.tm_year, to.tm_mon, to.tm_mday, wd[to.tm_wday])
    str_day = "%d.%02d.%02d期 星期%s" % (to.tm_year, to.tm_mon, to.tm_mday, wd[to.tm_wday])
    return str_day


def draw_lsj_img(file_name, day_comment, title, cont):
    font_day_comment = ImageFont.truetype("SourceHanSansCN-Regular.ttf",24)
    font_title = ImageFont.truetype("chuti.ttf",24)
    font_cont = ImageFont.truetype("putong.ttf",24)
    im = Image.open(file_name)
    draw = ImageDraw.Draw(im)
    str_day = get_date_desc() + " " + day_comment
    draw.text((80,335),str_day, fill=(100,100,100),font=font_day_comment)
    n_align = 22
    title_arr = auto_align(title, n_align)
    hi = 0
    for title in title_arr:
        draw.text((55,387 + hi),title, fill=(0,0,0),font=font_title)
        draw.text((55,387 + hi),title, fill=(0,0,0),font=font_title)
        draw.text((55,387 + hi),title, fill=(0,0,0),font=font_title)
        hi += 50

    cont_arr = auto_align(cont, n_align)
    hi = 0
    for cont in cont_arr:
        draw.text((55,387 + hi),cont, fill=(40,40,40),font=font_cont)
        hi += 50

    sio = StringIO.StringIO()
    im.save(sio, 'jpeg')
    sio.seek(0)
    return sio.read()

class LSJHandler(tornado.web.RequestHandler):
    def post(self):
        day_comment = self.get_argument("day_comment")
        title = self.get_argument("title")
        cont = self.get_argument("cont")
        #self.render("user.html",username=user_name,email=user_email,website=user_website,language=user_language)
        data = draw_lsj_img("LSJ.jpg", day_comment, title, cont)
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
    draw.text((143,490),str_day, fill=(100,100,100),font=font_day_comment)

    title_arr = title.strip().replace('\r', '\n').replace('\n\n', '\n').split('\n')
    hi = 0
    dh = 65
    h0 = 587
    x0 = 65
    for title in title_arr:
        draw.text((x0, h0 + hi),title, fill=(0,0,0),font=font_title)
        draw.text((x0, h0 + hi),title, fill=(0,0,0),font=font_title)
        draw.text((x0, h0 + hi),title, fill=(0,0,0),font=font_title)
        hi += dh

    cont_arr = cont.strip().replace('\r', '\n').replace('\n\n', '\n').split('\n')
    hi = 0
    for cont in cont_arr:
        draw.text((x0,h0 + hi),cont, fill=(0,0,0),font=font_cont)
        hi += dh
    sio = StringIO.StringIO()
    im.save(sio, 'jpeg')
    sio.seek(0)
    return sio.read()


class PAIHandler(tornado.web.RequestHandler):
    def post(self):
        day_comment = self.get_argument("day_comment")
        title = self.get_argument("title")
        cont = self.get_argument("cont")
        #self.render("user.html",username=user_name,email=user_email,website=user_website,language=user_language)
        data = draw_pai_img("PAI.jpg", day_comment, title, cont)
        self.write(data)
        self.set_header("Content-type", "image/jpg")
    def get(self):
        self.render("index_pai.html")

def draw_baic_img(file_name, day_comment, title, cont):
    font_day_comment = ImageFont.truetype("SourceHanSansCN-Regular.ttf",30)
    #font_title=font_cont= ImageFont.truetype("SourceHanSansCN-Regular.ttf",34)
    font_title=font_cont= ImageFont.truetype("hanyi_zhongsong.ttf",34)
    im = Image.open(file_name)
    draw = ImageDraw.Draw(im)
    str_day = get_date_desc_baic() + " " + day_comment
    draw.text((373,190),str_day, fill=(255,255,255),font=font_day_comment)

    title_arr = title.strip().replace('\r', '\n').replace('\n\n', '\n').split('\n')
    hi = 0
    dh = 61
    h0 = 387
    x0 = 75
    for title in title_arr:
        draw.text((x0, h0 + hi),title, fill=(0,0,0),font=font_title)
        draw.text((x0, h0 + hi),title, fill=(0,0,0),font=font_title)
        draw.text((x0, h0 + hi),title, fill=(0,0,0),font=font_title)
        hi += dh

    cont_arr = cont.strip().replace('\r', '\n').replace('\n\n', '\n').split('\n')
    hi = 0
    for cont in cont_arr:
        draw.text((x0,h0 + hi),cont, fill=(90,90,90),font=font_cont)
        hi += dh
    sio = StringIO.StringIO()
    im.save(sio, 'jpeg')
    sio.seek(0)
    return sio.read()



def draw_baic1_img(file_name, day_comment, title, cont):
    font_day_comment = ImageFont.truetype("SourceHanSansCN-Regular.ttf",24)
    font_title = font_cont= ImageFont.truetype("SourceHanSansCN-Regular.ttf",35)
    #font_title = ImageFont.truetype("chuti.ttf",38)
    #font_cont = ImageFont.truetype("putong.ttf",38)
    im = Image.open(file_name)
    draw = ImageDraw.Draw(im)
    #to = time.localtime(time.time())
    #wd = ["一","二","三","四","五","六","日"]
    #str_day = "%d.%02d.%02d星期%s" % (to.tm_year, to.tm_mon, to.tm_mday, wd[to.tm_wday])
    #str_day = "%d年%d月%d日 %02d:%02d:%02d 星期%s" % (to.tm_year, to.tm_mon, to.tm_mday, to.tm_hour, to.tm_min, to.tm_sec, wd[to.tm_wday])
    str_day = get_date_desc()
    draw.text((343,190),str_day, fill=(255,255,255),font=font_day_comment)

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
    sio = StringIO.StringIO()
    im.save(sio, 'jpeg')
    sio.seek(0)
    return sio.read()



class BAICHandler(tornado.web.RequestHandler):
    def post(self):
        day_comment = u''#self.get_argument("day_comment")
        title = u''#self.get_argument("title")
        cont = self.get_argument("cont")
        #self.render("user.html",username=user_name,email=user_email,website=user_website,language=user_language)
        data = draw_baic_img("BAIC.jpg", day_comment, title, cont)
        self.write(data)
        self.set_header("Content-type", "image/jpg")
    def get(self):
        self.render("index_baic.html")



handlers = [
    (r"/", IndexHandler),
    (r"/user", UserHandler),
    (r"/t", TestHandler),
    (r"/lsj", LSJHandler),
    (r"/pai", PAIHandler),
    (r"/baic", BAICHandler),
]

template_path = os.path.join(os.path.dirname(__file__),"template")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers, template_path)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
