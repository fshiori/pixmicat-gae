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
from model.pixmicat import ResizeImage

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
        return None #Don't need resize
    new_width = int(now_width * resizeP)
    new_height = int(now_height * resizeP)
    pic.resize(width=new_width, height=new_height)
    pic = pic.execute_transforms(output_encoding=images.JPEG)
    return pic

def _getImageSize(pic):
    pic = images.Image(pic)
    width = pic.width
    height = pic.height
    return {'width':width, 'height':height}

def _miniature(key_name, type=1):
    #type 1 is Post, 2 is Reply
    if settings.CACHE_RESIZE_PIC:
        cached_pic = memcache.get(key_name, namespace='ResizeImage')
        if cached_pic:
            return cached_pic
    if settings.STORAGE_RESIZE_PIC:
        entity = ResizeImage.get_by_key_name(key_name)
    else:
        entity = None
    if not entity:
        entity = Image.get_by_key_name(key_name)
        if not entity:
            return
        pic = _resize(entity.pic, type)
        if not pic:
            return entity.pic
        if settings.STORAGE_RESIZE_PIC:
            pic_data = _getImageSize(pic)
            tmpEntity = ResizeImage(key_name=key_name, post=entity.post, width=pic_data.get('width'), height=pic_data.get('height'), pic=db.Blob(pic))
            tmpEntity.put()
            #entity.resize = True
            #entity.put()
    else:
        pic = entity.pic
    if settings.CACHE_RESIZE_PIC:
        memcache.set(key_name, pic, namespace='ResizeImage')
    return pic
    
class ImageController(BaseController):
    
    def index(self):
        pass
    
    def get(self):
        key_name = self.params.get('id')
        if settings.CACHE_PIC:
            cached_pic = memcache.get(key_name)
            if cached_pic:
                self.render(image=cached_pic)
                return
        entity = Image.get_by_key_name(key_name)
        if not entity:
            self.render(text='Exception: %s' % 'No Image!')
            return
        if settings.CACHE_PIC:
            memcache.set(key_name, entity.pic, namespace='Image')
        self.render(image=entity.pic)
        
    def show(self):
        key_name = self.params.get('id')
        pic = _miniature(key_name, type=1)
        if not pic:
            self.render(text='Exception: %s' % 'No Image!')
            return            
        self.render(image=pic)
        
    def showReply(self):
        key_name = self.params.get('id')
        pic = _miniature(key_name, type=2)
        if not pic:
            self.render(text='Exception: %s' % 'No Image!')
            return            
        self.render(image=pic)              
                