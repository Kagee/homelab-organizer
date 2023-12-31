from django.conf import settings

from django.urls import path #, include
from django.conf.urls.static import static
from django.contrib import admin

from django.shortcuts import redirect
from django.conf.urls import include

from .views import JohnSearchView
from django.http import HttpResponse

urlpatterns = [
    path('', lambda request: redirect('inventory/', permanent=False)),
    path("admin/", admin.site.urls, name="admin"),
    path('search/', JohnSearchView.as_view(), name="search"),
    path('inventory/', include('inventory.urls')),
    path('loader/', include('loader.urls')),
    # django-select2
    path("select2/", include("django_select2.urls")),
    # Return empty for favicon
    path('favicon.ico', lambda request: HttpResponse()),
    # Serve static contect through Django
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
