import os
import urllib
import webapp2

from controllers import server 


application = webapp2.WSGIApplication([
    ('/', server.MainPage),
    ('/sign', server.Guestbook),
], debug=True)


# Extra Hanlder like 404 500 etc
def handle_404(request, response, exception):
    response.write('Page not found (404).')
    response.set_status(404)

application.error_handlers[404] = handle_404