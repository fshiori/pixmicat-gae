# -*- coding: utf-8 -*-
import webapp2

from urls import routes
from settings import DEBUG, config
from handler import BaseHandler
from models import Pixmicat

class MainPage(BaseHandler):
    def get(self):
        self.render_response('index.html')

app = webapp2.WSGIApplication(routes=routes, debug=DEBUG, config=config)