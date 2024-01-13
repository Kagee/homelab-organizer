from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path

from . import views
from .views import (
    AttachementSearchView,
    OrderDetailView,
    OrderItemDetailView,
    StockItemCreate,
    StockItemDetail,
    StockItemUpdate,
    TagAutoResponseView,
)

urlpatterns = [*[
    path("admin/", admin.site.urls, name="admin"),
    # path("admin/", hlo_admin.urls, name="admin"),  # noqa: ERA001
    # django-debug-toolbar
    path("__debug__/", include("debug_toolbar.urls")),
    # django-select2
    path("select2/", include("django_select2.urls")),
    # This is used by the tag-selector on stockitem-create
    path(
        "select2/fields/tags.json",
        TagAutoResponseView.as_view(),
        name="stockitem-tag-auto-json",
    ),
    # Return empty for favicon
    path("favicon.ico", lambda _request: HttpResponse()),
    path(
        "",
        views.index,
        name="index",
    ),
    path("search/", AttachementSearchView.as_view(), name="attachementsearch"),
    path("stockitem/list", views.stockitem_list, name="stockitem-list"),
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
    path("orderitems/list", views.product_list, name="orderitems-list"),
    path(
        "orderitems/detail/<int:pk>",
        OrderItemDetailView.as_view(),
        name="orderitem",
    ),
    path(
        "order/detail/<int:pk>", OrderDetailView.as_view(), name="order-detail",
    ),
    # Serve static content through Django
], *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)]

handler404 = "hlo.views.render404"
