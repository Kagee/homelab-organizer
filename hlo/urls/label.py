from django.urls import path

from hlo.views import (
    label_print_item_size,
    label_print_orderitem,
    label_print_sha1_size,
    label_print_storage,
    label_render_item_size,
    label_render_orderitem,
    label_render_sha1_size,
    label_render_storage,
    sha1_redirect,
)

urls = [  # Label stuff
    path(
        "sha1/<str:sha1>",
        sha1_redirect,
        name="sha1-redirect",
    ),
    path(
        "label/render/<str:sha1>_size_<int:multiplier>.png",
        label_render_sha1_size,
        name="label-render-sha1-size",
    ),
    path(
        "label/print/<str:sha1>_size_<int:multiplier>.png",
        label_print_sha1_size,
        name="label-print-sha1-size",
    ),
    path(
        "label/render/orderitem/<int:pk>.png",
        label_render_orderitem,
        name="label-render-orderitem",
    ),
    path(
        "label/render/item/<int:multiplier>/<int:pk>.png",
        label_render_item_size,
        name="label-render-item-size",
    ),
    path(
        "label/print/item/<int:multiplier>/<int:pk>.png",
        label_print_item_size,
        name="label-print-item-size",
    ),
    path(
        "label/print/orderitem/<int:pk>",
        label_print_orderitem,
        name="label-print-orderitem",
    ),
    path(
        "label/render/storage/<int:pk>.png",
        label_render_storage,
        name="label-render-storage",
    ),
    path(
        "label/render/storage/<int:pk>",
        label_print_storage,
        name="label-print-storage",
    ),
]

__all__ = [
    "urls",
]
