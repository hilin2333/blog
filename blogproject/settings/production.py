from .common import *

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY','26hyddx2xd_(1^!h4kidh-5i%%h9h*2$84nld!=668fccb(g_y')

ALLOWED_HOSTS = ['localhost','.silencecorner.com']
DEBUG = False


# django anymail grid
ANYMAIL = {
    "SENDGRID_API_KEY":" your SENDGRID  KEY",
}
EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
DEFAULT_FROM_EMAIL = "hilin2333@gmail.com"

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
