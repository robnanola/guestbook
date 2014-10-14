import os 
import jinja2
from filters import slugify
from filters import unslugify

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'../views')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

JINJA_ENVIRONMENT.filters['slugify'] = slugify
JINJA_ENVIRONMENT.filters['unslugify'] = unslugify

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

APP_ID = 'guestbook-test-733'