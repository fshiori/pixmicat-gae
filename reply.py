# -*- coding: utf-8 -*-
import logging

from webapp2 import uri_for

from urls import routes
from settings import DEBUG, config
from handler import BaseHandler
from models import Pixmicat

class ReplyPage(BaseHandler):
    def get(self, res=''):
        if not res:
            return self.redirect(uri_for('main'))
        page = 1
        self.render_response('test.html')
