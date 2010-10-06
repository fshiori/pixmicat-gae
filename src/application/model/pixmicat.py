from google.appengine.ext import db
from gaeo.model import BaseModel, SearchableBaseModel

class Pixmicat(BaseModel):
    username = db.StringProperty()
    uid = db.StringProperty()
    email = db.StringProperty()
    title = db.StringProperty()
    content = db.TextProperty()
    pic = db.BlobProperty()
    tag = db.StringListProperty()
    password = db.StringProperty()
    createtime = db.DateTimeProperty()
    replytime = db.DateTimeProperty()
    postip = db.StringProperty()   
    mainpost = db.SelfReferenceProperty()
