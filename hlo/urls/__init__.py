from django.urls import path

from hlo.urls import commontree, items, label, utils
from hlo.urls.utils import handler404
from hlo.views import (
    AttachementSearchView,
    item_search,
)

urlpatterns = [
    *[  # This is where dev happens
        path(
            "search/items",
            item_search,
            name="item-search",
        ),
        path(
            "search/attachements",
            AttachementSearchView.as_view(),
            name="attachement-search",
        ),
    ],
    *label.urls,
    *items.urls,
    *utils.urls,
    *commontree.urls,
]
__all__ = ["urlpatterns", "handler404"]
