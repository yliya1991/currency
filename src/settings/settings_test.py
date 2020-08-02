from settings.settings import *

SECRET_KEY = 'x4u^#b!c)-!fbokvl1#(yaf!z_5k$4)do^(3cghe2)8qftja3y'
DEBUG = False
ALLOWED_HOSTS = ['*']

CELERY_ALWAYS_EAGER = CELERY_TASK_ALWAYS_EAGER = True  # run celery tasks as functions

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db-test.sqlite3'),
    }
}


EMAIL_BACKEND = 'django.core.mail.outbox'
