# -*- coding: utf-8 -*-
from google.appengine.ext import db

class Counter(db.Model):
    count = db.IntegerProperty(required=True, default=0)
    
class BaseImage(db.Model):
    post = db.ReferenceProperty()
    width = db.IntegerProperty()
    height = db.IntegerProperty()
    image = db.BlobProperty()
    
class Image(BaseImage):
    pass
    
class ThumbImage(BaseImage):
    pass

class Pixmicat(db.Model):
    index = db.IntegerProperty(required=True) 
    name = db.StringProperty()
    postid = db.StringProperty()
    email = db.StringProperty()
    title = db.StringProperty()
    content = db.TextProperty()
    image = db.BooleanProperty()
    tags = db.StringListProperty()
    password = db.StringProperty()
    createtime = db.DateTimeProperty(auto_now_add=True)
    replytime = db.DateTimeProperty(auto_now_add=True)
    postip = db.StringProperty()   
    mainpost = db.SelfReferenceProperty()
    count = db.IntegerProperty(required=True, default=0) 