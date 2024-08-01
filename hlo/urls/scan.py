from django.urls import path

from hlo.views.scan import (
    WebappView,
    manifest_json,
    move_item_to_storage,
    move_storage_into_storage,
)

urls = [
    path(
        "scan",
        WebappView.as_view(),
        name="scan",
    ),
    path(
        "scan/<str:code1_get>",
        WebappView.as_view(),
        name="scan-one-code",
    ),
    path(
        "scan/<str:code1_get>/<str:code2_get>",
        WebappView.as_view(),
        name="scan-two-codes",
    ),
    path(
        "scan/move-item-to-storage",
        move_item_to_storage,
        name="move-item-to-storage",
    ),
    path(
        "scan/move-storage-into-storage",
        move_storage_into_storage,
        name="move-store-into-storage",
    ),
    path(
        "manifest.json",
        manifest_json,
    ),
]

__all__ = [
    "urls",
]
