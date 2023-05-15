from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django_cron import CronJobManager

CRON_CLASSES = [
    'products.cron.ProductCronJob',  # replace myapp with the name of your Django app
    # add more cron job classes if needed
]

cron_manager = CronJobManager(CRON_CLASSES)

urlpatterns = [
    path('', include('authentication.urls')),
    path('', include('products.urls')),  
    path('admin/', admin.site.urls),
]
handler404 = "core.views.page_not_found_view"

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)