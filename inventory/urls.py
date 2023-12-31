from django.urls import path

from . import views
from .views import (
    StockItemCreate,
    StockItemDetail,
    StockItemList,
    StockItemUpdate,
    ColorTagAutoResponseView,
)

urlpatterns = [
    path(
        "",
        views.index,
        name="inventory-index",
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
]
