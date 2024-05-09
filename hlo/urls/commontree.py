from django.urls import path

from hlo.views import (
    StorageCreateView,
    StorageDetailView,
    StorageListView,
    StorageUpdateView,
)

urls = [
    path(
        "storage/create/<int:parent>",
        StorageCreateView.as_view(),
        name="storage-create-parent",
    ),
    path(
        "storage/create",
        StorageCreateView.as_view(),
        name="storage-create",
    ),
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
]

__all__ = [
    "urls",
]
