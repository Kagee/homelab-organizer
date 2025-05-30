from pathlib import Path

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import FileResponse
from django.urls import include, path

from hlo.views import (
    TagAutoResponseView,
    index,
    no_access,
)

urls = [
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
    path("admin/", admin.site.urls, name="admin"),
    path("__debug__/", include("debug_toolbar.urls")),
    path(
        "favicon.ico",
        lambda _: FileResponse(
            Path("static/images/logo/hlo-cc0-logo-favicon.ico").open("rb"),  # noqa: SIM115
        ),
    ),
    # django-select2-stuff
    path("select2/", include("django_select2.urls")),
    # This is used by the tag-selector on stockitem-create
    path(
        "select2/fields/tags.json",
        TagAutoResponseView.as_view(),
        name="stockitem-tag-auto-json",
    ),
    # Serve static content through Django
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]

handler404 = "hlo.views.render404"

__all__ = ["handler404", "urls"]
