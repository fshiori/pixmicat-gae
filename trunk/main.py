# -*- coding: utf-8 -*-
import webapp2

from urls import routes
from settings import DEBUG, config

app = webapp2.WSGIApplication(routes=routes, debug=DEBUG, config=config)