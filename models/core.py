from google.appengine.ext import ndb


class Greeting(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    rating = ndb.IntegerProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
