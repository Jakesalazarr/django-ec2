# core/storages.py
from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    location = 'media'  # or '' if you removed it
    file_overwrite = False
    default_acl = 'public-read'
    querystring_auth = False

    def _save(self, name, content):
        print(f"[DEBUG] Saving to S3: {name}")
        return super()._save(name, content)



