# -*- coding: utf-8 -*-
import cgi
import logging

from google.appengine.ext import db
from google.appengine.api import images
from google.appengine.api import memcache

from gaeo.controller import BaseController

import settings
from model.pixmicat import Pixmicat
from model.pixmicat import Image

def _resize(pic, type=1):
    #type 1 is Post, 2 is Reply
    if type == 1:
        limit_width = settings.MAX_W
        limit_height = settings.MAX_W
    else:
        limit_width = settings.MAX_RW
        limit_height = settings.MAX_RW
    pic = images.Image(pic)
    now_width = pic.width
    now_height = pic.height
    resizeP_width = 1
    resizeP_height = 1
    if now_width > limit_width:
        resizeP_width = float(limit_width) / now_width
    if now_height > limit_height:
        resizeP_height = float(limit_height) / now_height
    if resizeP_width < resizeP_height:
        resizeP = resizeP_width
    else:
        resizeP = resizeP_height
    if resizeP == 1:
        return pic
    new_width = int(now_width * resizeP)
    new_height = int(now_height * resizeP)
    pic.resize(width=new_width, height=new_height)
    pic = pic.execute_transforms(output_encoding=images.JPEG)
    return pic

class ImageController(BaseController):
    
    def index(self):
        pass
    
    def get(self):
        key_name = self.params.get('id')
        cached_pic = memcache.get(key_name)
        if cached_pic:
            self.render(image=cached_pic)
            return
        entity = Image.get_by_key_name(key_name)
        if not entity:
            self.render(text='Exception: %s' % 'No Image!')
            return
        memcache.set(key_name, entity.pic)
        self.render(image=entity.pic)
        
    def show(self):
        key_name = self.params.get('id')
        cached_pic = memcache.get(key_name)
        if cached_pic:
            self.render(image=cached_pic)
            return
        entity = Image.get_by_key_name(key_name)
        if not entity:
            self.render(text='Exception: %s' % 'No Image!')
            return       
        pic = _resize(entity.pic, type=1)
        memcache.set(key_name, pic)
        self.render(image=pic)
        
    def showReply(self):
        key_name = self.params.get('id')
        cached_pic = memcache.get(key_name)
        if cached_pic:
            self.render(image=cached_pic)
            return
        entity = Image.get_by_key_name(key_name)
        if not entity:
            self.render(text='Exception: %s' % 'No Image!')
            return       
        pic = _resize(entity.pic, type=2)
        memcache.set(key_name, pic)
        self.render(image=pic)               
                