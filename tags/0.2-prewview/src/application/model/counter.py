from google.appengine.ext import db
from gaeo.model import BaseModel, SearchableBaseModel

class Counter(BaseModel):
     count = db.IntegerProperty(required=True, default=0)