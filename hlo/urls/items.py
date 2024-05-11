from django.urls import path

from hlo.views import (
    OrderCreateView,
    OrderDetailView,
    OrderItemCreateView,
    OrderItemDetailView,
    OrderListView,
    ShopCreateView,
    ShopDetailView,
    ShopListView,
    StockItemCreate,
    StockItemDetail,
    StockItemUpdate,
    orderitem_filtered_list,
    stockitem_list,
)

urls = [
    # STOCKITEMS
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
    # ORDERITEMS
    path("orderitem/list", orderitem_filtered_list, name="orderitem-list"),
    path(
        "orderitem/detail/<int:pk>",
        OrderItemDetailView.as_view(),
        name="orderitem-detail",
    ),
    path(
        "orderitem/create",
        OrderItemCreateView.as_view(),
        name="orderitem-create",
    ),
    path(
        "orderitem/create/<int:pk>",
        OrderItemCreateView.as_view(),
        name="orderitem-create-order",
    ),
    # ORDERS
    path(
        "order/detail/<int:pk>",
        OrderDetailView.as_view(),
        name="order-detail",
    ),
    path(
        "order/create",
        OrderCreateView.as_view(),
        name="order-create",
    ),
    path(
        "order/create/<int:shop>",
        OrderCreateView.as_view(),
        name="order-create-shop",
    ),
    path(
        "order/list",
        OrderListView.as_view(),
        name="order-list",
    ),
    # SHOPS
    path(
        "shop/create",
        ShopCreateView.as_view(),
        name="shop-create",
    ),
    path(
        "shop/detail/<int:pk>",
        ShopDetailView.as_view(),
        name="shop-detail",
    ),
    path(
        "shop/list",
        ShopListView.as_view(),
        name="shop-list",
    ),
]

__all__ = [
    "urls",
]
