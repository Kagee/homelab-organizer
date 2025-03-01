from functools import partial

from django.urls import path

from hlo.views import (
    label_print_identicon_sha1,
    label_print_sha1_size,
    label_render_identicon_sha1,
    label_render_sha1_size,
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
        "label/render/<str:sha1>.png",
        partial(label_render_sha1_size, multiplier=4),
        name="label-render-sha1",
    ),
    path(
        "label/print/<str:sha1>_size_<int:multiplier>.png",
        label_print_sha1_size,
        name="label-print-sha1-size",
    ),
    path(
        "label/print/<str:sha1>.png",
        partial(label_print_sha1_size, multiplier=4),
        name="label-render-sha1",
    ),
    path(
        "label/identicon/print/<str:sha1>.png",
        label_print_identicon_sha1,
        name="label-print-identicon-sha1",
    ),
    path(
        "label/identicon/render/<str:sha1>.png",
        label_render_identicon_sha1,
        name="label-render-identicon-sha1",
    ),
]

__all__ = [
    "urls",
]
