from pathlib import Path

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import FileResponse
from django.urls import include, path

from hlo.urls import items, label, utils
from hlo.views import (
    AttachementSearchView,
    StorageDetailView,
    StorageListView,
    StorageUpdateView,
    TagAutoResponseView,
    index,
    item_search,
    no_access,
    sha1_redirect,
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
    *[  # Stock stuff, not ligely to change
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
    *label.urls,
    *items.urls,
    *utils.urls,
]

handler404 = "hlo.views.render404"
