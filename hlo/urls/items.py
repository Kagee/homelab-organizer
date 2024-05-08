from django.urls import path

from hlo.views import (
    OrderDetailView,
    OrderItemDetailView,
    StockItemCreate,
    StockItemDetail,
    StockItemUpdate,
    orderitem_filtered_list,
    stockitem_list,
)

urls = [  # Item stuff
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
        name="orderitem-detail",
    ),
    path(
        "order/detail/<int:pk>",
        OrderDetailView.as_view(),
        name="order-detail",
    ),
]

__all__ = [
    "urls",
]
