# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'babel.zip')

import webapp2

from urls import routes
from settings import DEBUG, config

app = webapp2.WSGIApplication(routes=routes, debug=DEBUG, config=config)