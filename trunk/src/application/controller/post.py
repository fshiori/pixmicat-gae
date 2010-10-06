# -*- coding: utf-8 -*-
import cgi

from google.appengine.ext import db

from gaeo.controller import BaseController

def _processUsername(username):
    import string
    import hashlib
    tmp = string.find(username,'◆')
    if tmp != -1:
        return string.replace(username, '◆', '◇')
    tmp = string.find(username,'#')
    if tmp == -1:
        return username
    tmp = username.split('#',1)
    username = tmp[0]
    stamp = tmp[1]
    if not stamp:
        return username
    m = hashlib.md5()
    m.update(stamp)
    stamp = m.hexdigest()[0:10]
    username = '%s◆%s' % (username, stamp)
    return username

def _processPostid(postip):
    import hashlib
    m = hashlib.md5()
    m.update(postip)
    postid = m.hexdigest()[0:8]
    return postid

class PostController(BaseController):
    def new(self):
        #print self.params
        username = self.params.get('name')
        #self.tmp = _processUsername(username)
        postip = self.request.remote_addr