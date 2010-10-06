import cgi

from google.appengine.ext import db

from gaeo.controller import BaseController


class PostController(BaseController):
    def new(self):
        #print self.params
        pass