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
        msgs = msgs.fetch(10, 10*p)
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