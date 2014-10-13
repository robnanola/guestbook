import urllib 

from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import json
import datetime

from conf import settings
from models import core as core_model


class jsonEncoder(json.JSONEncoder):
    """
    Converts ndb, datetime object to json.
    """
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        elif isinstance(obj, ndb.Model):
            return obj.to_dict()

        elif isinstance(obj, users.User):
            return obj.email()

        else:
            return json.JSONEncoder.default(self, obj)

# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

def guestbook_key(guestbook_name=settings.DEFAULT_GUESTBOOK_NAME):
    """
    Constructs a Datastore key for a Guestbook entity with guestbook_name.
    """
    return ndb.Key('Guestbook', guestbook_name)

class MainPage(webapp2.RequestHandler):

    def get(self):
        guestbook_name = self.request.get('guestbook_name',
                                          settings.DEFAULT_GUESTBOOK_NAME)
        greetings_query = core_model.Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-core_model.Greeting.date)
        greetings = greetings_query.fetch(10)

        greetings.reverse()


        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = settings.JINJA_ENVIRONMENT.get_template('/index.html')
        self.response.write(template.render(template_values))


class Guestbook(webapp2.RequestHandler):

    def post(self):
        guestbook_name = self.request.get('guestbook_name',
                                          settings.DEFAULT_GUESTBOOK_NAME)
        greeting = core_model.Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()

        self.response.out.write(json.dumps(greeting, cls=jsonEncoder))