# -*- coding: utf-8 -*-
import datetime
import logging
import cgi
import string
import hashlib
import random

from google.appengine.ext import db
from google.appengine.api import images

from gaeo.controller import BaseController
from gaeo.session.memcache import MemcacheSession 
import settings
from model.pixmicat import Pixmicat
from model.counter import Counter

def _processUsername(username):

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
    #m = hashlib.sha1()
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

def _createRandom(len=10):
    tmp = ''
    for i in range(len):
        tmp += random.choice('1234567890qwertyuiopasdfghjklzxcvbnm')
    return tmp

def _resize(pic):
    width = pic.width
    height = pic.height
    if width > 250 or height > 250:
        if width > height:
            rsize =  250.0 / width
        else:
            rsize =  250.0 / height
        width = int(width * rsize)
        height = int(height * rsize)
    return {'width':width, 'height':height}

def _resizeReply(pic):
    width = pic.width
    height = pic.height
    if width > 125 or height > 125:
        if width > height:
            rsize =  125.0 / width
        else:
            rsize =  125.0 / height
        width = int(width * rsize)
        height = int(height * rsize)
    return {'width':width, 'height':height}

def _getFileSize(pic):
    size = len(pic)
    size = size/1024
    return size

def _packData(msg, type=1):
    tmp = {}
    tmp['key'] = msg.key()
    tmp['content'] = msg.content
    tmp['createtime'] = msg.createtime
    tmp['email'] = msg.email
    tmp['index'] = msg.index
    tmp['pic'] = 0
    if msg.pic:
        tmp['pic'] = 1
        tmp['size'] = _getFileSize(msg.pic)
        pic = images.Image(msg.pic)
        tmp['width'] = pic.width
        tmp['height'] = pic.height
        if type == 1:
            d = _resize(pic)
        else:
            d = _resizeReply(pic)
        tmp['newwidth'] = d.get('width')
        tmp['newheight'] = d.get('height')
        tmp['resize'] = 0
        if tmp['width'] != tmp['newwidth'] or tmp['height'] != tmp['newheight']:
            tmp['resize'] = 1
    tmp['postid'] = msg.postid
    tmp['title'] = msg.title
    tmp['username'] = msg.username
    return tmp  

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
        if not password:
            password = _createRandom()
            session = MemcacheSession(self)
            session['password'] = password
            session.put()
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
        _setPostCounter()
        #self.savepassword = password
        self.redirect('/')
        
    def read(self):
        self.title = settings.TITLE
        key = self.params.get('id')
        self.key = key
        msg = Pixmicat.get(key)
        p = self.params.get('pages')
        if not p:
            p = 0
        else:
            p = int(p)
        #logging.info(p)
        session = MemcacheSession(self)
        savepassword = session.get('password')
        #logging.info(session)
        if savepassword:
            #logging.info("1")
            self.savepassword = savepassword  
        self.title = settings.TITLE
        totalpost = Counter.get_by_key_name('Post').count
        res = []
        tmp = _packData(msg)
        replies = Pixmicat.all()
        replies.filter('mainpost =', msg)
        replies.order('createtime')
        for reply in replies:
            tmp2 = _packData(reply, 2)
            res.append(tmp2)
        tmp['replies'] = res
        #posts.append(tmp)
        self.msgs = [tmp]
        pages = totalpost / 10
        self.pages = range(pages + 1)
        self.nowpage = p
        self.maxpage = pages
        #tz = tz_helper.timezone(settings.TIME_ZONE)
        #now = datetime.datetime.now(tz)
        #self.render(text='Exception: %s' % now)
    
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
            content = u'無內文'
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
        entity.count += 1
        entity.put()
        self.redirect('/')
        
    def noimg(self):
        self.title = settings.TITLE
        
    def delete(self):
        params = self.params.items()
        logging.info(params)
        for param in params:
            if param[1] == 'delete' and param[0] != 'pwd' and param[0] != 'action':
                logging.info(param)
                key = param[0]
                entity = Pixmicat.get(key)
                passwd = self.params.get('pwd')
                logging.info(entity.password)
                logging.info(passwd)
                if entity.password == passwd:
                    #onlyimgdel on
                    if self.params.get('onlyimgdel') == 'on':
                        entity.pic = None
                        entity.put()
                    else:
                        replies = Pixmicat.all()
                        replies.filter('mainpost =', entity)
                        for reply in replies:
                            reply.delete()
                        if entity.mainpost == None:
                            _setPostCounter(2)
                        entity.delete()
        self.redirect('/')

                
        