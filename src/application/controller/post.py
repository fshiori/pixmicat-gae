# -*- coding: utf-8 -*-
import datetime
import logging
import cgi

from google.appengine.ext import db

from gaeo.controller import BaseController

import settings
from model.pixmicat import Pixmicat
from model.counter import Counter

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

def _processTag(tags):
    tagslist = []
    tmps = tags.split(',')
    for tmp in tmps:
        tagslist.append(tmp)
    return tagslist

def _getCounter():
    ind = Counter.get_by_key_name('Pixmicat')
    if ind is None:
        ind = Counter(key_name='Pixmicat')
    ind.count += 1
    ind.put()
    return ind.count

class PostController(BaseController):
    
    def new(self):
        username = self.params.get('name')
        if username:
            username = _processUsername(username)
        else:
            username = '無名氏'
        postip = self.request.remote_addr
        postid = _processPostid(postip)
        email = self.params.get('email')
        title = self.params.get('sub')
        if not title:
            title = '無標題'
        content = self.params.get('com')
        if not content:
            content = u'無內文'
            #content = 'xxx'
        pic = self.params.get('upfile')
        tags = self.params.get('category')
        noimg = self.params.get('noimg')
        if tags:
            tags = _processTag(tags)
        password = self.params.get('pwd')
        index = _getCounter()
        data = Pixmicat(index=index, username=username, postid=postid, email=email, title=title, content=content, password=password, postip=postip)
        if pic:
            data.pic = db.Blob(pic)
        else:
            if noimg != 'on':
                self.redirect('/post/noimg')
                return
        if tags:
            data.tags = tags
        data.put()
        self.redirect('/')
        
    def read(self):
        key = self.params.get('id')
        self.key = key
    
    def reply(self):
        username = self.params.get('name')
        if username:
            username = _processUsername(username)
        else:
            username = '無名氏'
        postip = self.request.remote_addr
        postid = _processPostid(postip)
        email = self.params.get('email')
        title = self.params.get('sub')
        if not title:
            title = '無標題'
        content = self.params.get('com')
        if not content:
            content = '無內文'
        pic = self.params.get('upfile')
        tags = self.params.get('category')
        noimg = self.params.get('noimg')
        if tags:
            tags = _processTag(tags)
        password = self.params.get('pwd')
        index = _getCounter()
        key = self.params.get('id')
        entity = db.get(key)
        data = Pixmicat(mainpost = entity, index=index, username=username, postid=postid, email=email, title=title, content=content, password=password, postip=postip)
        if pic:
            data.pic = db.Blob(pic)
        else:
            if noimg != 'on':
                self.redirect('/post/noimg')
                return
        if tags:
            data.tags = tags
        data.put()
        if email != 'sage':
            now = datetime.datetime.now()
            entity.replytime = now
            entity.put()
        self.redirect('/')
        
    def noimg(self):
        self.title = settings.TITLE