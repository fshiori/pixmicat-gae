# -*- coding: utf-8 -*-
import datetime
import tz_helper

from gaeo.controller import BaseController
from google.appengine.ext import db

import settings
from model.pixmicat import Pixmicat

class WelcomeController(BaseController):
    """The default Controller

    You could change the default route in main.py
    """
    def index(self):
        """The default method

        related to templates/welcome/index.html
        """
        self.title = settings.TITLE
        
        msgs = Pixmicat.all()
        msgs.order('-replytime')
        msgs.fetch(10)
        self.msgs = msgs
        #tz = tz_helper.timezone(settings.TIME_ZONE)
        #now = datetime.datetime.now(tz)
        #self.render(text='Exception: %s' % now)
