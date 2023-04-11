import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

ENV = 'staging'

sentry_key = os.environ['SENTRY_KEY']
sentry_org = os.environ['SENTRY_ORGANISATION']
sentry_project = os.environ['SENTRY_PROJECT']
sentry_sdk.init(
    dsn=f"https://{sentry_key}@{sentry_org}.ingest.sentry.io/{sentry_project}",
    integrations=[
        CeleryIntegration(),
        DjangoIntegration(),
    ],
    # Associates users to errors
    send_default_pii=True,
    environment=ENV,
)

SECRET_KEY = os.environ["SECRET_KEY"]
DEBUG = True if os.environ["DEBUG"] == "True" else False

ALLOWED_HOSTS = [
    os.environ["DJANGO_HOST"],
]

CORS_ORIGIN_WHITELIST = (
    f"http://{os.environ['WEB_APP_HOST']}",
    f"https://{os.environ['WEB_APP_HOST']}",
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ["DATABASE_NAME"],
        'USER': os.environ["DATABASE_USER"],
        'PASSWORD': os.environ["DATABASE_PASSWORD"],
        'HOST': os.environ["DATABASE_HOST"],
        'PORT': os.environ["DATABASE_PORT"],
    }
}

# static files
STATIC_ROOT = '/app/static'

# AWS
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_S3_REGION_NAME = os.environ["AWS_S3_REGION_NAME"]
AWS_S3_DOMAIN = "s3.amazonaws.com"
AWS_MEDIA_BUCKET_NAME = os.environ["AWS_MEDIA_BUCKET_NAME"]
AWS_S3_CUSTOM_DOMAIN = f"{AWS_MEDIA_BUCKET_NAME}.{AWS_S3_DOMAIN}"
AWS_S3_FILE_OVERWRITE = False
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}

DEFAULT_FILE_STORAGE = "fix_the_news.custom_storage.S3MediaStorage"
