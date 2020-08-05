"""GoogleCloudStorage extensions suitable for handing Django's
Static and Media files.

Requires following settings:
MEDIA_URL, GS_MEDIA_BUCKET_NAME
STATIC_URL, GS_STATIC_BUCKET_NAME

In addition to
https://django-storages.readthedocs.io/en/latest/backends/gcloud.html
"""

from django.conf import settings
from storages.backends.gcloud import GoogleCloudStorage
from storages.utils import setting
from urllib.parse import urljoin


class GoogleCloudMediaFileStorage(GoogleCloudStorage):
      """
      Google file storage class which gives a media file path from MEDIA_URL not google generated one.
      """
      bucket_name = setting('GS_BUCKET_NAME')

      def url(self, name):
          """
          Gives correct MEDIA_URL and not google generated url.
          """
          return urljoin(settings.MEDIA_URL, name)
