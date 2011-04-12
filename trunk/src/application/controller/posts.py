# -*- coding: utf-8 -*-
import cgi
import hashlib
import string
import random

from google.appengine.ext import db

from gaeo.controller import BaseController
from gaeo.session.memcache import MemcacheSession

import settings
import image
from model.pixmicat import Pixmicat
from model.counter import Counter
from model.pixmicat import Image
from model.pixmicat import ResizeImage

def _tranStamp(i):
    i = i % 62
    if i >= 0 and i <= 9: #0-9 48-57 -> 0-9
        return chr(i + 48)
    elif i >= 10 and i <= 35: #A-Z 65-90 -> 10-35
        return chr(i + 55)
    elif i >= 36 and i <= 61: #a-z 97-122 -> 36-61
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
    is_cap = _processCap(username, email)
    cap = ''
    if is_cap:
        cap = settings.CAP_SUFFIX
    stamp = ''
    if len(tmp) > 1:
        stamp = tmp[1]
    if not stamp:
        return username
    stamp = _createHash(stamp)
    username = '%s◆%s%s' % (username, stamp, cap)
    return username

def _processCap(username, email=''):
    if not settings.CAP_ENABLE:
        return False
    if email == '#' + settings.CAP_PASS and username == settings.CAP_NAME:
        return True
    return False

def _processPostid(postip):
    return _createHash(postip)[0:8]

def _processTag(tags):
    tagslist = []
    tmps = tags.split(',')
    for tmp in tmps:
        s = unicode(tmp, 'utf-8')
        tagslist.append(s)
    return tagslist

def _getCounter():
    ind = Counter.get_by_key_name('Pixmicat')
    if ind is None:
        ind = Counter(key_name='Pixmicat')
    ind.count += 1
    ind.put()
    return ind.count

def _setPostCounter(type=1):
    ind = Counter.get_by_key_name('Post')
    if ind is None:
        ind = Counter(key_name='Post')
    if type == 1:
        ind.count += 1
    else:
        ind.count -= 1
    ind.put()
    return ind.count

def _createPassword(len=8):
    tmp = ''
    for i in range(len):
        tmp += _tranStamp(random.randint(0,62))
    return tmp
    
class PostsController(BaseController):
    
    def index(self):
        pass
    
    def new(self):
        username = self.params.get('name').encode('utf-8')
        email = self.params.get('email').encode('utf-8')
        if username:
            username = _processUsername(username, email)
        else:
            username = settings.DEFAULT_NONAME
        username = unicode(username, 'utf-8')
        postip = self.request.remote_addr
        postid = _processPostid(postip)
        title = self.params.get('sub').encode('utf-8')
        if not title:
            title = settings.DEFAULT_NOTITLE
        title = unicode(title, 'utf-8')
        content = self.params.get('com').encode('utf-8')
        if not content:
            content = settings.DEFAULT_NOCOMMENT
        content = unicode(content, 'utf-8')
        pic = self.params.get('upfile')
        tags = self.params.get('category').encode('utf-8')
        noimg = self.params.get('noimg')
        if tags:
            tags = _processTag(tags)
        else:
            tags = ""
        password = self.params.get('pwd')
        if not password:
            password = _createPassword()
            session = MemcacheSession(self)
            session['password'] = password
            session.put()
            #password = password.encode('utf-8')
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
            pic_data = image.getImageSize(pic)
            tmpEntity = Image(key_name=key_name, post=data, width=pic_data.get('width'), height=pic_data.get('height'), pic=db.Blob(pic))
            #pic_data = image.getImageSize(pic)
            tmpEntity.put()
            image.createMiniature(key_name, 1)
        #self.savepassword = password
        #logging.info("1")
        self.redirect('/')
    
    def reply(self):
        pass