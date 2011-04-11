# -*- coding: utf-8 -*-
import cgi
import logging

from google.appengine.ext import db
from google.appengine.api import images

from gaeo.controller import BaseController
from gaeo.session.memcache import MemcacheSession

import settings
from model.pixmicat import Pixmicat
from model.counter import Counter

def _packData(msg, type=1):
    tmp = {}
    tmp['key'] = msg.key()
    tmp['content'] = msg.content
    tmp['createtime'] = msg.createtime
    tmp['email'] = msg.email
    tmp['index'] = msg.index
    tmp['pic'] = 0
    if msg.pic:
        image = Image.get_by_key_name(str(msg.index))
        tmp['pic'] = 1
        tmp['size'] = len(tttt.pic)
        tmp['width'] = tttt.width
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
        msgs = Pixmicat.all()
        msgs.filter('mainpost =', None) 
        msgs.order('-replytime')
        msgs = msgs.fetch(settings.PAGE_DEF, settings.PAGE_DEF * page)
        posts = []
        for msg in msgs:
            res = []
            pack_msg = _packData(msg)
            replies = Pixmicat.all()
            replies.filter('mainpost =', msg)
            replies.order('createtime')
            for reply in replies:
                pack_res = _packData(reply, 2)
                res.append(pack_res)
            pack_msg['replies'] = res
            posts.append(pack_msg)
        self.msgs = posts
        totalpage = totalpost / 10
        self.pages = range(pages + 1)
        self.nowpage = page
        self.maxpage = totalpage
        #tz = tz_helper.timezone(settings.TIME_ZONE)
        #now = datetime.datetime.now(tz)
        #self.render(text='Exception: %s' % now)