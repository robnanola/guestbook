"""
	@author: robnanola
	@description: Contains the list of url to be used by the application.

"""

from controllers import server


ROUTING = [
    ('/', server.MainPage),
    ('/sign', server.Guestbook),
]