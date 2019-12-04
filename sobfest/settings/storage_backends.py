from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class MediaStorage(S3Boto3Storage):
    location = settings.AWS_FILE_PATH
    file_overwrite = True
    default_acl = 'public-read'
