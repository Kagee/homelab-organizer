from django.urls import path

from hlo.views import (
    OrderCreateView,
    OrderDetailView,
    OrderItemCreateView,
    OrderItemDetailView,
    OrderItemUpdateView,
    OrderListView,
    OrderSimpleCreateView,
    OrderUpdateView,
    ShopCreateView,
    ShopDetailView,
    ShopListView,
    ShopUpdateView,
    StockItemCreate,
    StockItemDetail,
    StockItemUpdate,
    orderitem_filtered_list,
    orderitem_hide,
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
    path(
        "stockitem/create",
        StockItemCreate.as_view(),
        name="stockitem-create",
    ),
    # ORDERITEMS
    path("orderitem/list", orderitem_filtered_list, name="orderitem-list"),
    path(
        "orderitem/detail/<int:pk>",
        OrderItemDetailView.as_view(),
        name="orderitem-detail",
    ),
    path(
        "orderitem/hide/<int:pk>/<str:hide>",
        orderitem_hide,
        name="orderitem-hide",
    ),
    path(
        "orderitem/create",
        OrderItemCreateView.as_view(),
        name="orderitem-create",
    ),
    path(
        "orderitem/create/<int:order>",
        OrderItemCreateView.as_view(),
        name="orderitem-create-order",
    ),
    path(
        "orderitem/update/<int:pk>",
        OrderItemUpdateView.as_view(),
        name="orderitem-update",
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
        "order/create_simple/<int:shop>",
        OrderSimpleCreateView.as_view(),
        name="order-create-simple",
    ),
    path(
        "order/update/<int:pk>",
        OrderUpdateView.as_view(),
        name="order-update",
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
        "shop/update/<int:pk>",
        ShopUpdateView.as_view(),
        name="shop-update",
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
