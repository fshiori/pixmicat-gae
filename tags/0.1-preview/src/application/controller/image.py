# -*- coding: utf-8 -*-
import logging

from google.appengine.api import images

from gaeo.controller import BaseController

from model.pixmicat import Pixmicat

class ImageController(BaseController):
    
    def index(self):
        pass
    
    def get(self):
        key = self.params.get('id')
        entity = Pixmicat.get(key)
        self.render(image=entity.pic)
        
    def resize(self):
        key = self.params.get('id')
        entity = Pixmicat.get(key)
        pic = images.Image(entity.pic)
        width = pic.width
        height = pic.height
        if width > 250 or height > 250:
            if width > height:
                rsize =  250.0 / width
            else:
                rsize =  250.0 / height
            newwidth = int(width * rsize)
            newheight = int(height * rsize)
            pic.resize(width=newwidth, height=newheight)
            pic = pic.execute_transforms(output_encoding=images.JPEG)
            self.render(image=pic)
            return
        self.render(image=entity.pic)
        
    def resizeReply(self):
        key = self.params.get('id')
        entity = Pixmicat.get(key)
        pic = images.Image(entity.pic)
        width = pic.width
        height = pic.height
        if width > 125 or height > 125:
            if width > height:
                rsize =  125.0 / width
            else:
                rsize =  125.0 / height
            newwidth = int(width * rsize)
            newheight = int(height * rsize)
            pic.resize(width=newwidth, height=newheight)
            pic = pic.execute_transforms(output_encoding=images.JPEG)
            self.render(image=pic)
            return
        self.render(image=entity.pic)               
                