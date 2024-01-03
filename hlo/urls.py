from django.conf import settings

from django.urls import path  # , include
from django.conf.urls.static import static
from django.contrib import admin

from django.shortcuts import redirect
from django.conf.urls import include
from django.http import HttpResponse

from . import views
from .views import (
    StockItemCreate,
    StockItemDetail,
    StockItemList,
    StockItemUpdate,
    ColorTagAutoResponseView,
    JohnSearchView,
    OrderItemDetailView,
    OrderDetailView,
    OrderListView,
)


urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("search/", JohnSearchView.as_view(), name="search"),
    # django-select2
    path("select2/", include("django_select2.urls")),
    # Return empty for favicon
    path("favicon.ico", lambda request: HttpResponse()),
    path(
        "",
        views.index,
        name="index",
    ),
    path("stockitem/list", StockItemList.as_view(), name="stockitem-list"),
    path(
        "stockitem/detail/<int:pk>",
        StockItemDetail.as_view(),
        name="stockitem-detail",
    ),
    path(
        "stockitem/update/<int:pk>",
        StockItemUpdate.as_view(),
        name="stockitem-update",
    ),
    path(
        "stockitem/create/<str:fromitems>",
        StockItemCreate.as_view(),
        name="stockitem-create-from",
    ),
    # This is used by the tag-selector on stockitem-create
    path(
        "stockitem/tags.json",
        ColorTagAutoResponseView.as_view(),
        name="stockitem-tag-auto-json",
    ),
    path("orderitems/list", views.product_list, name="orderitems-list"),
    path(
        "orderitems/detail/<int:pk>",
        OrderItemDetailView.as_view(),
        name="orderitem",
    ),
    path("order/list", OrderListView.as_view(), name="orders-list"),
    path(
        "order/detail/<int:pk>", OrderDetailView.as_view(), name="order-detail"
    ),
    # Serve static contect through Django
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
