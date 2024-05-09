from django.urls import path

from hlo.views import (
    label_print_orderitem,
    label_print_storage,
    label_render_orderitem,
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
        "label/render/orderitem/<int:pk>.png",
        label_render_orderitem,
        name="label-render-orderitem",
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
