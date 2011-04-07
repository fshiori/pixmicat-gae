# -*- coding: utf-8 -*-
import datetime
import tz_helper

from gaeo.controller import BaseController
from google.appengine.ext import db
from google.appengine.api import images

import settings
from model.pixmicat import Pixmicat

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

def _getFileSize(pic):
    size = len(pic)
    size = size/1024
    return size

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
        msgs.filter('mainpost =', None) 
        msgs.order('-replytime')
        msgs.fetch(10)
        posts = []
        for msg in msgs:
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
                d = _resize(pic)
                tmp['newwidth'] = d.get('width')
                tmp['newheight'] = d.get('height')
                tmp['resize'] = 0
                if tmp['width'] != tmp['newwidth'] or tmp['height'] != tmp['newheight']:
                    tmp['resize'] = 1
            tmp['postid'] = msg.postid
            tmp['title'] = msg.title
            tmp['username'] = msg.username
            replies = Pixmicat.all()
            replies.filter('mainpost =', msg)
            replies.order('createtime')
            tmp['replies'] = replies
            posts.append(tmp)
        self.msgs = posts
        #tz = tz_helper.timezone(settings.TIME_ZONE)
        #now = datetime.datetime.now(tz)
        #self.render(text='Exception: %s' % now)
