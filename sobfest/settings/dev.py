from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zc59=a%ahi5x-+8)e290&-e*&co8cy*3d#ye)7am6^$w_)elnt'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

print('DEV ' * 8)
try:
    from .local import *
except ImportError:
    pass
