from storages.backends.s3boto3 import S3Boto3Storage

from django.conf import settings


class S3MediaStorage(S3Boto3Storage):
    bucket_name = settings.AWS_MEDIA_BUCKET_NAME
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN
