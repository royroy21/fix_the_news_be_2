from .base import *

ENV = 'local'

# CORS_ORIGIN_WHITELIST = (
#     "http://localhost:3000",
# )

ALLOWED_HOSTS = (
    "localhost",
)
CORS_ALLOW_HEADERS = "*"
CORS_ALLOW_ALL_ORIGINS = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'docker',
        'PASSWORD': 'docker',
        'HOST': 'db',
        'PORT': 5432,
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'level': 'WARNING',
            'handlers': ['console'],
        },
        'fix_the_news': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Add a local_custom.py file to import
# settings used locally not saved to GIT.
try:
    from .local_custom import *  # noqa
except ModuleNotFoundError:
    pass
