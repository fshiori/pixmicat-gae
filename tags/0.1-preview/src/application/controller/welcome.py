# -*- coding: utf-8 -*-
import datetime
import logging

import tz_helper
from gaeo.controller import BaseController
from gaeo.session.memcache import MemcacheSession
from google.appengine.ext import db
from google.appengine.api import images

import settings
from model.pixmicat import Pixmicat
from model.counter import Counter

def _resize(pic):
    width = pic.width
    height = pic.height
    if width > 250 or height > 250:
        if width > height:
            rsize =  250.0 / width
        else:
            rsize =  250.0 / height
        width = int(width * rsize)
        height = int(height * rsize)
    return {'width':width, 'height':height}

def _resizeReply(pic):
    width = pic.width
    height = pic.height
    if width > 125 or height > 125:
        if width > height:
            rsize =  125.0 / width
        else:
            rsize =  125.0 / height
        width = int(width * rsize)
        height = int(height * rsize)
    return {'width':width, 'height':height}

def _getFileSize(pic):
    size = len(pic)
    size = size/1024
    return size

def _packData(msg, type=1):
    tmp = {}
    tmp['key'] = msg.key()
    tmp['content'] = msg.content
    tmp['createtime'] = msg.createtime
    tmp['email'] = msg.email
    tmp['index'] = msg.index
    tmp['pic'] = 0
    if msg.pic:
        tmp['pic'] = 1
        tmp['size'] = _getFileSize(msg.pic)
        pic = images.Image(msg.pic)
        tmp['width'] = pic.width
        tmp['height'] = pic.height
        if type == 1:
            d = _resize(pic)
        else:
            d = _resizeReply(pic)
        tmp['newwidth'] = d.get('width')
        tmp['newheight'] = d.get('height')
        tmp['resize'] = 0
        if tmp['width'] != tmp['newwidth'] or tmp['height'] != tmp['newheight']:
            tmp['resize'] = 1
    tmp['postid'] = msg.postid
    tmp['title'] = msg.title
    tmp['username'] = msg.username
    return tmp

class WelcomeController(BaseController):
    """The default Controller

    You could change the default route in main.py
    """
    def index(self):
        """The default method

        related to templates/welcome/index.html
        """
        p = self.params.get('pages')
        if not p:
            p = 0
        else:
            p = int(p)
        #logging.info(p)
        session = MemcacheSession(self)
        savepassword = session.get('password')
        #logging.info(session)
        if savepassword:
            #logging.info("1")
            self.savepassword = savepassword  
        self.title = settings.TITLE
        totalpost = Counter.get_by_key_name('Post').count
        msgs = Pixmicat.all()
        msgs.filter('mainpost =', None) 
        msgs.order('-replytime')
        msgs = msgs.fetch(10, 10*p)
        #logging.info(len(msgs))
        posts = []
        for msg in msgs:
            res = []
            tmp = _packData(msg)
            replies = Pixmicat.all()
            replies.filter('mainpost =', msg)
            replies.order('createtime')
            for reply in replies:
                tmp2 = _packData(reply, 2)
                res.append(tmp2)
            tmp['replies'] = res
            posts.append(tmp)
        self.msgs = posts
        pages = totalpost / 10
        self.pages = range(pages + 1)
        self.nowpage = p
        self.maxpage = pages
        #tz = tz_helper.timezone(settings.TIME_ZONE)
        #now = datetime.datetime.now(tz)
        #self.render(text='Exception: %s' % now)
