from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'circle_test',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'USERNAME': 'circleci',
        'PASSWORD': 'circleci',
    }
}
