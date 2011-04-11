# -*- coding: utf-8 -*-
import cgi
import logging
from datetime import datetime

from google.appengine.ext import db
from google.appengine.api import images
from google.appengine.api import memcache

from gaeo.controller import BaseController
from gaeo.session.memcache import MemcacheSession

import tz_helper
import settings
from model.pixmicat import Pixmicat
from model.counter import Counter
from model.pixmicat import Image
from model.pixmicat import ResizeImage

def _packData(msg, type=1):
    tz = tz_helper.timezone(settings.TIME_ZONE)
    tmp = {}
    #tmp['key'] = msg.key()
    tmp['content'] = msg.content
    local_time = msg.createtime + tz.utcoffset(msg.createtime)
    tmp['createtime'] = local_time
    tmp['email'] = msg.email
    tmp['index'] = msg.index
    tmp['pic'] = 0
    if msg.pic:
        image = None
        if settings.CACHE_PIC:
            cached_pic = memcache.get(str(msg.index))
            if cached_pic:
                image = pickle.loads(cached_pic)
        if not image:
            image = Image.get_by_key_name(str(msg.index))
        tmp['pic'] = 1
        tmp['size'] = len(image.pic)
        tmp['width'] = image.width
        tmp['height'] = image.height
        image = None
        if settings.CACHE_RESIZE_PIC:
            cached_pic = memcache.get(str(msg.index))
            if cached_pic:
                image = pickle.loads(cached_pic)
        if not image:
            image = ResizeImage.get_by_key_name(str(msg.index))
        tmp['newwidth'] = image.width
        tmp['newheight'] = image.height
        tmp['resize'] = 0
        if tmp['width'] != tmp['newwidth'] or tmp['height'] != tmp['newheight']:
            tmp['resize'] = 1
    tmp['postid'] = msg.postid
    tmp['title'] = msg.title
    tmp['username'] = msg.username
    return tmp

class ShowController(BaseController):
    
    def index(self):
        self.title = settings.TITLE
        page = self.params.get('id')
        if not page:
            page = 0
        else:
            page = int(page)
        session = MemcacheSession(self)
        password = session.get('password')
        if password:
            self.password = password
        totalpost = 0
        entity = Counter.get_by_key_name('Post')
        if entity:
            totalpost = entity.count
        posts = Pixmicat.all()
        posts.filter('mainpost =', None) 
        posts.order('-replytime')
        posts = posts.fetch(settings.PAGE_DEF, settings.PAGE_DEF * page)
        list_posts = []
        for post in posts:
            list_reply = []
            pack_msg = _packData(post)
            replies = Pixmicat.all()
            replies.filter('mainpost =', post)
            replies.order('createtime')
            for reply in replies:
                pack_res = _packData(reply, 2)
                list_reply.append(pack_res)
            pack_msg['replies'] = list_reply
            list_posts.append(pack_msg)
        self.msgs = list_posts
        totalpage = totalpost / 10
        self.pages = range(totalpage + 1)
        self.nowpage = page
        self.maxpage = totalpage