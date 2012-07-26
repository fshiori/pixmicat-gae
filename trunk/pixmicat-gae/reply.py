# -*- coding: utf-8 -*-
import logging

from webapp2 import uri_for

from urls import routes
from settings import DEBUG, config
from handler import BaseHandler
from models import Pixmicat

class ReplyPage(BaseHandler):
    def get(self, res='', page_num=''):
        if not res:
            return self.redirect(uri_for('main'))
        page = page_num if page_num else 'RE_PAGE_MAX'
        if not(page == 'all' or page=='RE_PAGE_MAX'):
            page = int(page_num)
        #updatelog($res, $page); // 實行分頁
        self.render_response('test.html')
