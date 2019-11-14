import dj_database_url
import django_heroku
from .base import *

DEBUG = False

try:
    from .local import *
except ImportError:
    pass

DATABASES['default'] = dj_database_url.config()
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

import django_heroku
django_heroku.settings(locals())

