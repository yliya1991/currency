SECRET_KEY = 'x4u^#b!c)-!fbokvl1#(yaf!z_5k$4)do^(3cghe2)8qftja3y'

DEBUG = True
ALLOWED_HOSTS = ['*']

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'email@gmail.com'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'currency',
        'USER': 'currency',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '',
    }
}
