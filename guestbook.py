import os
import urllib
import webapp2

from urls import ROUTING

application = webapp2.WSGIApplication(ROUTING, debug=True)


# 404 handler
def handle_404(request, response, exception):
    response.write('<h1>Page does not exists.</h1>')
    response.set_status(404)

application.error_handlers[404] = handle_404