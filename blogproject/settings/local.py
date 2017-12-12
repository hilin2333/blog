from .common import *

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY',
                            '26hyddx2xd_(1^!h4kidh-5i%%h9h*2$84nld!=668fccb(g_y')
DEBUG = True
ALLOWED_HOSTS = ['*']
# debug toolbar
INTERNAL_IPS = ['127.0.0.1','0.0.0.0']
JQUERY_URL = ''

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INSTALLED_APPS += [
    'debug_toolbar',
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


DEFAULT_FROM_EMAIL = "hilin2333@gmail.com"

DATABASES = {
   'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test',
        'USER': 'test',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}