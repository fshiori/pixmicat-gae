# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'babel.zip')

import webapp2

from urls import routes
from settings import DEBUG, config

config['webapp2_extras.jinja2'] = {'environment_args': { 'extensions': ['jinja2.ext.i18n'] }}
app = webapp2.WSGIApplication(routes=routes, debug=DEBUG, config=config)