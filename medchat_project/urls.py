from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from rest_framework import routers
from django.http import JsonResponse
from django.conf import settings


def health(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health),
    path("api/accounts/", include("accounts.urls")),
    path("api/", include("uploads.urls")),

]
# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
