# -*- coding: utf-8 -*-
import webapp2

from urls import routes
from settings import DEBUG, config
from handler import BaseHandler
from models import Pixmicat

class MainPage(BaseHandler):
    def get(self, page_num=0):
        context = {}
        context['config'] = self.app.config
        q = Pixmicat.all()
        q.order('-replytime')
        PAGE_DEF = self.app.config.get('PAGE_DEF')
        threads = q.fetch(limit=PAGE_DEF, offset=page_num * PAGE_DEF)
        self.render_response('index.html', **context)

app = webapp2.WSGIApplication(routes=routes, debug=DEBUG, config=config)