from django.conf import settings

from django.urls import path #, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import include

from .views import JohnSearchView

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path('search/', JohnSearchView.as_view(), name="search"),
    path('inventory/', include('inventory.urls')),
    path('loader/', include('loader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
