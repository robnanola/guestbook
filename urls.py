"""
	@author: robnanola
	@description: Contains the list of url to be used by the application.

"""

from controllers import server
from controllers import admin


ROUTING = [
    ('/', server.MainPageHandler),
    ('/sign', server.GuestbookHandler),
    ('/user/([^/]+)/comments', server.UserCommentsHandler),
    ('/hotel/([^/]+)', server.HotelCommentsHandler),
    ('/hotel/([^/]+)/sign', server.HotelGuestbookHandler),
    ('/admin/hotels', admin.HotelAdminHandler),
    ('/admin/upload', admin.UploadHotelHandler),
]