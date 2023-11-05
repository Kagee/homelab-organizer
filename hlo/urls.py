from django.conf import settings

from django.urls import path #, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import include, url

from .views import JohnSearchView

urlpatterns = [
    #path("", include("order_scraper.urls")),
    #path("orders/", OrderListView.as_view(), name="order-list"),
    path("admin/", admin.site.urls),
    path('search/', JohnSearchView.as_view(), name="search"),
    url('', include('inventory.urls')),
    path('search2/', include('haystack.urls')),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
