# -*- coding: utf-8 -*-
import cgi
import hashlib

from google.appengine.ext import db

from gaeo.controller import BaseController

import settings
from model.pixmicat import Pixmicat
from model.counter import Counter
from model.pixmicat import Image
from model.pixmicat import ResizeImage

def _tranStamp(i):
    #a-z 97-122 -> 36-61
    #0-9 48-57 -> 0-9
    #A-Z 65-90 -> 10-35
    i = i % 62
    if i >= 0 and i <= 9:
        return chr(i + 48)
    elif i >= 10 and i <= 35:
        return chr(i + 55)
    elif i >= 36 and i <= 61:
        return chr(i + 61)
    return ''

def _createHash(s):
    key = s + settings.IDSEED
    m = hashlib.md5()
    m.update(key)
    stamp = m.hexdigest() # 32
    hash = ''
    for i in range(10):
        tmp = 0
        for j in range(10):
            tmp += ord(stamp[i+j])
        hash += _tranStamp(tmp)
    return hash[0:10]

def _processUsername(username, email=''):
    username = string.replace(username, '★', '')
    username = string.replace(username, '◆', '◇')
    tmp = username.split('#',1)
    username = tmp[0]
    stamp = ''
    if len(tmp) > 1:
        stamp = tmp[1]
    if not stamp:
        return username
    stamp = _createHash(stamp)
    username = '%s◆%s' % (username, stamp)
    return username

def _processCap(username, email=''):
    if not settings.CAP_ENABLE:
        return username
    
    
class PostsController(BaseController):
    
    def index(self):
        pass
    
    def new(self):
        username = self.params.get('name')
        if username:
            username = username.encode('utf-8')
            username = _processUsername(username)
        else:
            username = '無名氏'
        username = unicode(username, 'utf-8')
        postip = self.request.remote_addr
        postip = postip.encode('utf-8')
        postid = _processPostid(postip)
        postid = unicode(postid, 'utf-8')
        email = self.params.get('email')
        if email:
            email = email.encode('utf-8')
        title = self.params.get('sub')
        if not title:
            title = '無標題'
        else:
            title = title.encode('utf-8')
        title = unicode(title, 'utf-8')
        content = self.params.get('com')
        if not content:
            content = '無內文'
            #content = 'xxx'
        else:
            content = content.encode('utf-8')
        content = unicode(content, 'utf-8')
        pic = self.params.get('upfile')
        tags = self.params.get('category')
        noimg = self.params.get('noimg')
        if tags:
            tags = _processTag(tags)
        else:
            tags = u""
        password = self.params.get('pwd')
        if not password:
            password = _createRandom()
            session = MemcacheSession(self)
            session['password'] = password
            session.put()
            password = password.encode('utf-8')
        index = _getCounter()
        #data = Pixmicat(index=index, username=username, postid=postid, email=email, title=title, content=content, password=password, postip=postip)
        data = Pixmicat(key_name=str(index), index=index)
        data.username=username
        data.postid=postid
        data.email=email
        data.title=title
        #logging.info(content)
        #data.content=db.Text(content, encoding="utf-8")
        data.content=db.Text(content)
        data.password=password
        data.postip=postip
        #logging.info("2")
        if pic:
            data.pic = True
        else:
            if noimg != 'on':
                self.redirect('/post/noimg')
                return
        if tags:
            data.tags = tags
        #logging.info(data)
        data.put()
        _setPostCounter()
        if pic:
            key_name = str(index)
            pic_data = _getImageSize(pic)
            tmpEntity = Image(key_name=key_name, post=data, width=pic_data.get('width'), height=pic_data.get('height'), pic=db.Blob(pic))
            pic_data = _getImageSize(pic)
            tmpEntity.put()
        #self.savepassword = password
        #logging.info("1")
        self.redirect('/')
    
    def reply(self):
        pass