from django.urls import path
from django.views.generic.base import TemplateView

from hlo import views
from hlo.urls import commontree, items, label, scan, utils
from hlo.urls.utils import handler404
from hlo.views import (
    AttachementSearchView,
    item_search,
)


class AboutView(TemplateView):
    template_name = "common/about.html"


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
        path(
            "about",
            AboutView.as_view(),
            name="about",
        ),
        path(
            "test",
            views.test,
            name="about",
        ),
    ],
    *label.urls,
    *items.urls,
    *utils.urls,
    *commontree.urls,
    *scan.urls,
]
__all__ = ["urlpatterns", "handler404"]
