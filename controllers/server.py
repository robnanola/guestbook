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
    Encodes ndb, datetime objects to json.
    """
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        elif isinstance(obj, ndb.Model):
            obj_dct = obj.to_dict()
            
            #add id to the return dict 
            obj_dct['id'] = obj.key.id()

            return obj_dct

        elif isinstance(obj, users.User):
            return obj.email()

        else:
            return json.JSONEncoder.default(self, obj)


def guestbook_key(guestbook_name=settings.DEFAULT_GUESTBOOK_NAME):
    """
    Constructs a Datastore key for a Guestbook entity with guestbook_name.
    """
    return ndb.Key('Guestbook', guestbook_name)


class BaseHandler(webapp2.RequestHandler):
    """
    User aware handler
    """

    @webapp2.cached_property
    def user(self):
        return users.get_current_user()

    def render_template(self, template_name, context_data=None):
        if not context_data:
            context_data = {}

        context_data['user'] = self.user

        template = settings.JINJA_ENVIRONMENT.get_template(template_name)
        self.response.write(template.render(context_data))

    def json_response(self, data):
        #add data
        json_data = json.dumps(data, cls=jsonEncoder)
        self.response.out.write(json_data)



class MainPage(BaseHandler):

    def get(self):
        guestbook_name = self.request.get('guestbook_name',
                                          settings.DEFAULT_GUESTBOOK_NAME)
        greetings_query = core_model.Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-core_model.Greeting.date)
        
        greetings = greetings_query.fetch(10)


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

        self.render_template('/index.html', context_data=template_values)


class Guestbook(BaseHandler):

    def post(self):
        guestbook_name = self.request.get('guestbook_name',
                                          settings.DEFAULT_GUESTBOOK_NAME)

        if self.request.get('content'):
            # create or update ??        
            if self.request.get('id'):
                greeting = core_model.Greeting.get_by_id(int(self.request.get('id')),
                parent=guestbook_key(guestbook_name))

                # check if we are updating greetings of the same user
                if greeting.author != self.user:
                    
                    self.abort(404)

            else:
                greeting = core_model.Greeting(parent=guestbook_key(guestbook_name))

                if self.user:
                    greeting.author = self.user
            greeting.content = self.request.get('content')
            greeting.put()

            self.json_response(greeting)

        else:
            self.json_response({})