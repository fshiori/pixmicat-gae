# -*- coding: utf-8 -*-
import string
import datetime
import logging

from google.appengine.api import images

from tz_helper import timezone
from handler import BaseHandler
from models import Pixmicat

class IndexPage(BaseHandler):
    def get(self, page_num=0):
        #如果瀏覽器支援XHTML標準MIME就輸出
        #todo
        #有啟動Gzip
        #todo
        context = {}
        context['config'] = self.app.config
        q = Pixmicat.all()
        q.order('-replytime')
        PAGE_DEF = self.app.config.get('PAGE_DEF')
        threads = q.fetch(limit=PAGE_DEF, offset=page_num * PAGE_DEF)
        #預測過舊文章和將被刪除檔案
        #todo
        context['formtop'] = True
        context['max_file_size'] = self.app.config.get('MAX_KB') * 1024
        context['allow_upload_ext'] = string.replace(self.app.config.get('ALLOW_UPLOAD_EXT'), '|', ', ')
        if self.app.config.get('STORAGE_LIMIT'):
            pass #todo
        for thread in threads:
            res_start = thread.count - self.app.config.get('RE_DEF') + 1
            if res_start < 1:
                res_start = 1
            res_amount = self.app.config.get('RE_DEF')
            hidden_reply = res_start - 1
            q = Pixmicat.all()
            q.filter('mainpost =', thread)
            q.order('createtime')
            posts = q.fetch(limit=res_amount, offset=res_start-1)
            for post in posts:
                name = post.name
        self.render_response('index.html', **context)
        
    def post(self):
        #self.request.get('content')
        name = self.request.get('name')
        email = self.request.get('email')
        sub = self.request.get('sub')
        com = self.request.get('com')
        pwd = self.request.get('pwd')
        category = self.request.get('category')
        upfile = self.request.get('upfile')
        ip = self.request.remote_addr
        tz = timezone(self.app.config.get('TIME_ZONE'))
        #logging.info(len(upfile))
        #try:
            
        self.render_response('index.html', **context)
        
