from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    # Add your other URL patterns here
]

# Only serve media files locally during development when not using S3
if settings.DEBUG and not os.environ.get('USE_S3', 'True') == 'True':
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)