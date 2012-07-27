# -*- coding: utf-8 -*-
from tz_helper import timezone
from handler import BaseHandler
from models import Pixmicat

class PostsPage(BaseHandler):
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