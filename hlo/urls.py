from django.conf import settings

from django.urls import path #, include
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    #path("", include("order_scraper.urls")),
    #path("orders/", OrderListView.as_view(), name="order-list"),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
