from pathlib import Path

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import FileResponse
from django.urls import include, path

from .views import (
    AttachementSearchView,
    OrderDetailView,
    OrderItemDetailView,
    StockItemCreate,
    StockItemDetail,
    StockItemUpdate,
    StorageDetailView,
    StorageListView,
    StorageUpdateView,
    TagAutoResponseView,
    index,
    item_search,
    label_print_orderitem,
    label_render_orderitem,
    no_access,
    orderitem_filtered_list,
    sha1_redirect,
    stockitem_list,
)

urlpatterns = [
    *[  # This is where dev happens
        path(
            "storage/list",
            StorageListView.as_view(),
            name="storage-list",
        ),
        path(
            "storage/detail/<int:pk>",
            StorageDetailView.as_view(),
            name="storage-detail",
        ),
        path(
            "storage/update/<int:pk>",
            StorageUpdateView.as_view(),
            name="storage-update",
        ),
        path(
            "sha1/<str:sha1>",
            sha1_redirect,
            name="sha1-redirect",
        ),
        path(
            "search/items",
            item_search,
            name="item-search",
        ),
    ],
    *[  # Label stuff
        path(
            "label/render/orderitem/<int:pk>.png",
            label_render_orderitem,
            name="label-render-orderitem",
        ),
        path(
            "label/print/orderitem/<int:pk>",
            label_print_orderitem,
            name="label-print-orderitem",
        ),
    ],
    *[  # Item stuff
        path("stockitem/list", stockitem_list, name="stockitem-list"),
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
        path("orderitem/list", orderitem_filtered_list, name="orderitem-list"),
        path(
            "orderitem/detail/<int:pk>",
            OrderItemDetailView.as_view(),
            name="orderitem",
        ),
        path(
            "order/detail/<int:pk>",
            OrderDetailView.as_view(),
            name="order-detail",
        ),
    ],
    *[  # Stock stuff, not ligely to change
        path("admin/", admin.site.urls, name="admin"),
        # path("admin/", hlo_admin.urls, name="admin"),  # noqa: ERA001
        # django-debug-toolbar
        path("__debug__/", include("debug_toolbar.urls")),
        path(
            "favicon.ico",
            lambda _: FileResponse(
                Path("static/images/logo/hlo-cc0-logo-favicon.ico").open("rb"),  # noqa: SIM115
            ),
        ),
        path(
            "",
            index,
            name="index",
        ),
        path(
            "no_access",
            no_access,
            name="no_access",
        ),
        path(
            "search/attachements",
            AttachementSearchView.as_view(),
            name="attachement-search",
        ),
    ],
    *[  # django-select2-stuff
        path("select2/", include("django_select2.urls")),
        # This is used by the tag-selector on stockitem-create
        path(
            "select2/fields/tags.json",
            TagAutoResponseView.as_view(),
            name="stockitem-tag-auto-json",
        ),
    ],
    # Serve static content through Django
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]

handler404 = "hlo.views.render404"
