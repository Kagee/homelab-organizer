import logging

from django.http import HttpResponse
from django.urls import path
from django.views.generic.base import TemplateView

from hlo.urls import commontree, items, label, scan, utils
from hlo.urls.utils import handler404
from hlo.views import (
    AttachmentSearchView,
    TagDetailView,
    TagItemListView,
    TagListView,
    item_search,
    items_with_tags,  # noqa: F401
)

logger = logging.getLogger(__name__)


class AboutView(TemplateView):
    template_name = "common/about.html"


def tag_list(_request):
    tags = None
    s = ""
    for tag in tags:
        s += f"{tag}" + "<br>"
        logger.debug(tag)
        logger.debug(tag.taggit_taggeditem_items.count())
        logger.debug(dir(tag))
    return HttpResponse(s)


def items_with_tags_list(_request):
    return HttpResponse("Hello world")


urlpatterns = [
    *[  # This is where dev happens
        path(
            "tags/list",
            TagListView.as_view(),
            name="tag-list",
        ),
        path(
            "tags/detail/<int:pk>",
            TagDetailView.as_view(),
            name="tag-detail",
        ),
        path(
            "tags/items",
            TagItemListView.as_view(),
            name="tag-item",
        ),
        path(
            "search/items",
            item_search,
            name="item-search",
        ),
        path(
            "search/attachments",
            AttachmentSearchView.as_view(),
            name="attachment-search",
        ),
        path(
            "about",
            AboutView.as_view(),
            name="about",
        ),
    ],
    *label.urls,
    *items.urls,
    *utils.urls,
    *commontree.urls,
    *scan.urls,
]
__all__ = ["handler404", "urlpatterns"]
