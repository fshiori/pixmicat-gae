# -*- coding: utf-8 -*-
import string

import webapp2

from urls import routes
from settings import DEBUG, config
from handler import BaseHandler
from models import Pixmicat

class MainPage(BaseHandler):
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
        
    def 

app = webapp2.WSGIApplication(routes=routes, debug=DEBUG, config=config)