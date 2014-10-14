import urllib 
import webapp2
import json
import datetime

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import memcache

from conf import settings
from models import core as core_model
from filters import unslugify

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

        elif isinstance(obj, ndb.Key):
            return obj.id()

        else:
            return json.JSONEncoder.default(self, obj)


def guestbook_key(guestbook_name=settings.DEFAULT_GUESTBOOK_NAME):
    """
    Constructs a Datastore key for a Guestbook entity with guestbook_name.
    """
    return ndb.Key('Guestbook', guestbook_name)


def get_hotels(always_new=False):
    """
    store/gets hotel list in memcache.
    """
    hotels = memcache.get('hotels')

    if not hotels or always_new == True:
        hotels = core_model.Hotel.query().order(core_model.Hotel.name).fetch()
        memcache.set('hotels', hotels)

    return hotels

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



class MainPageHandler(BaseHandler):

    def get(self):
        
        hotels = get_hotels()

        self.render_template('/index.html', context_data={'hotels':hotels})


class GuestbookHandler(BaseHandler):

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

            if self.request.get('rating') or self.request.get('rating') not in  ('0',''):
                greeting.rating = int(self.request.get('rating'))

            greeting.content = self.request.get('content')
            greeting.put()

            self.json_response(greeting)

        else:
            self.json_response({})


class HotelGuestbookHandler(BaseHandler):

    def post(self, hotel_name):
        hotel_name = unslugify(hotel_name)
        guestbook_name = self.request.get('guestbook_name',
                                          settings.DEFAULT_GUESTBOOK_NAME)

        hotel = core_model.Hotel.query(core_model.Hotel.name==hotel_name).get()
        hotel_key = ndb.Key(core_model.Hotel, hotel.key.id())

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

            if self.request.get('rating') or self.request.get('rating') not in  ('0',''):
                greeting.rating = int(self.request.get('rating'))

            greeting.hotel = hotel_key
            greeting.content = self.request.get('content')
            greeting.put()

            self.json_response(greeting)

        else:
            self.json_response({})



class UserCommentsHandler(BaseHandler):

    def get(self, email):

        guestbook_name = self.request.get('guestbook_name',
                                          settings.DEFAULT_GUESTBOOK_NAME)

        user = users.User(email)
        greetings = core_model.Greeting.query(
                core_model.Greeting.author==user
            ).order(-core_model.Greeting.date).fetch()



        self.render_template('user/comments.html', context_data={'greetings':greetings})


class HotelCommentsHandler(BaseHandler):

    def get(self, hotel_name):
        hotel_name = unslugify(hotel_name)
        guestbook_name = self.request.get('guestbook_name',
                                          settings.DEFAULT_GUESTBOOK_NAME)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'


        hotel = core_model.Hotel.query(core_model.Hotel.name==hotel_name).get()
        hotel_key = ndb.Key(core_model.Hotel, hotel.key.id())
        greetings = core_model.Greeting.query(core_model.Greeting.hotel==hotel_key
            ).order(-core_model.Greeting.date).fetch()

        template_values = {
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
            'hotel':hotel
        }

        self.render_template('hotel/comments.html', context_data=template_values)

