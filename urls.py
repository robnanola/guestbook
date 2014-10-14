"""
	@author: robnanola
	@description: Contains the list of url to be used by the application.

"""

from controllers import server


ROUTING = [
    ('/', server.MainPageHandler),
    ('/sign', server.GuestbookHandler),
    ('/user/([^/]+)/comments', server.UserCommentsHandler),
]