import os 
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'../views')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

print os.path.join(os.path.dirname(__file__),'../views'),'<<<<'

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'
