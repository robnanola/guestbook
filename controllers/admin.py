import urllib 

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import memcache

import webapp2
import json
import datetime
import csv

from conf import settings
from models import core as core_model
from .server import BaseHandler
from .server import guestbook_key
from .server import get_hotels
from blobiterator import BlobIterator


class HotelAdminHandler(BaseHandler):

    def get(self):

        hotels = get_hotels(always_new=True)

        upload_url = blobstore.create_upload_url('/admin/upload')

        self.render_template('/admin/hotels.html', context_data={'hotels':hotels, 'upload_url':upload_url})


class UploadHotelHandler(blobstore_handlers.BlobstoreUploadHandler):

    def post(self):

        FIELDS = ['name','address1', 'address2', 'contact_nos']

        upload_files = self.get_uploads('hotel_file')
        hotel_reader = blobstore.BlobReader(upload_files[0].key())
        hotel_iterator = BlobIterator(hotel_reader)
        reader = csv.DictReader(hotel_iterator, fieldnames=FIELDS)

        for h in reader:
            h['parent'] = guestbook_key(settings.DEFAULT_GUESTBOOK_NAME)
            hotel = core_model.Hotel(**h)

            hotel.put()

        #update hotels list in memcache
        memcache.set('hotels', core_model.Hotel.query().order(core_model.Hotel.name).fetch())

        self.redirect('/admin/hotels' )

