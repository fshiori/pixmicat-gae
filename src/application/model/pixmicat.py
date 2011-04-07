from google.appengine.ext import db
from gaeo.model import BaseModel, SearchableBaseModel

class Pixmicat(BaseModel):
    index = db.IntegerProperty(required=True)
    username = db.StringProperty()
    postid = db.StringProperty()
    email = db.StringProperty()
    title = db.StringProperty()
    content = db.TextProperty()
    pic = db.BlobProperty()
    tags = db.StringListProperty()
    password = db.StringProperty()
    createtime = db.DateTimeProperty(auto_now_add=True)
    replytime = db.DateTimeProperty(auto_now_add=True)
    postip = db.StringProperty()   
    mainpost = db.SelfReferenceProperty()
