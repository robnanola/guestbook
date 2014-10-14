from google.appengine.ext import ndb


class Greeting(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    author = ndb.UserProperty()
    hotel = ndb.KeyProperty(kind='Hotel', indexed=True)
    content = ndb.StringProperty(indexed=False)
    rating = ndb.IntegerProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)



class Hotel(ndb.Model):
	"""
	Model that holds hotel info
	"""
	name = ndb.StringProperty()
	address1 = ndb.StringProperty()
	address2 = ndb.StringProperty()
	contact_nos = ndb.StringProperty()
