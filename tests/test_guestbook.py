import unittest
import json
import ast

import webapp2
import webtest

from google.appengine.ext import db
from google.appengine.ext import testbed

from conf import settings
from controllers import server
from guestbook import application
from models import core as core_model


class BaseTestWrapper(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.setup_env(app_id=settings.APP_ID)
        self.testbed.activate()

        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_user_stub()
        self.testapp = webtest.TestApp(application)


    def tearDown(self):
        self.testbed.deactivate()


class TestMain(BaseTestWrapper):

    def testMainPage(self):
        """
        index page only allows GET method.
        """
        response = self.testapp.get('/')
        self.assertEqual(response.status_int, 200)

        response = self.testapp.post('/',params={}, expect_errors=True)
        self.assertEqual(response.status_int, 405)

        response = self.testapp.put('/', params={}, expect_errors=True)
        self.assertEqual(response.status_int, 405)

        response = self.testapp.delete('/', params={}, expect_errors=True)
        self.assertEqual(response.status_int, 405)


class TestGuestBook(BaseTestWrapper):

    def testSaveGreeting(self):
        """
        check if it saves correctly.
        """

        response = self.testapp.post('/sign', params={'content':'test1'}, expect_errors=True )

        greetings = core_model.Greeting.query()
        response_dict = json.loads(response.body)

        self.assertEqual(greetings.count(), 1)
        self.assertEqual(greetings.get().content,'test1')


    def testEmptyGreetingContent(self):
        """
        don't allow blank contents
        """
        
        response1 = self.testapp.post('/sign', params={'content':''}, expect_errors=True )
        greetings1 = core_model.Greeting.query()
        self.assertEqual(greetings1.count(), 0)


    def testUpdateGreeting(self):
        """
        update greeting content
        """

        greeting = core_model.Greeting(parent=server.guestbook_key(settings.DEFAULT_GUESTBOOK_NAME))
        greeting.content = "test_content"

        greeting.put()

        response1 = self.testapp.post(
                                '/sign', 
                                params={'content':'updated_content', 'id':greeting.key.id()}, 
                                expect_errors=True )

        response_dict = json.loads(response1.body)

        greetings = core_model.Greeting.query()

        self.assertEqual(greetings.count(), 1)
        self.assertEqual(greetings.get().content, 'updated_content')


    def testUpdateBlankGreeting(self):
        """
        update blank greeting content
        """

        greeting = core_model.Greeting(parent=server.guestbook_key(settings.DEFAULT_GUESTBOOK_NAME))
        greeting.content = "test_content"

        greeting.put()

        response1 = self.testapp.post(
                                '/sign', 
                                params={'content':'', 'id':greeting.key.id()}, 
                                expect_errors=True )

        response_dict = json.loads(response1.body)

        greetings = core_model.Greeting.query()

        self.assertEqual(greetings.count(), 1)
        self.assertEqual(greetings.get().content, 'test_content')


