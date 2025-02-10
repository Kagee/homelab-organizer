import logging

from django.db.models import Count, Max, Min, Value
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from taggit.models import Tag

logger = logging.getLogger(__name__)


class TagListView(ListView):
    """TagListView cloud display."""

    """
    queryset2 = (
        Tag.objects.annotate(
            item_count=Count("taggit_taggeditem_items"),
        )
        .annotate(
            min_item_count=Min("item_count"),
            max_item_count=Max("item_count"),
        )
        .order_by("-item_count")
    )
    """

    template_name = "tag/list.html"
    context_object_name = "page_obj"

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        if len(ctx["page_obj"]):
            return {
                "max_item_count": ctx["page_obj"][0].max_item_count,
                "min_item_count": ctx["page_obj"][0].min_item_count,
                **ctx,
            }
        return {
            "max_item_count": 0,
            "min_item_count": 0,
            **ctx,
        }

    def get_queryset(self):
        qs = Tag.objects.annotate(
            item_count=Count("taggit_taggeditem_items"),
        )
        max_ic = min_ic = None
        for tag in qs:
            if not max_ic:
                max_ic = tag.item_count
                min_ic = tag.item_count
                logger.debug("min: %s, max: %s", min_ic, max_ic)
                continue
            max_ic = max(max_ic, tag.item_count)
            min_ic = min(min_ic, tag.item_count)
            logger.debug("min: %s, max: %s", min_ic, max_ic)
        if max_ic is None:
            max_ic = 0
            min_ic = 0
        return qs.annotate(
            max_item_count=Value(max_ic),
            min_item_count=Value(min_ic),
        ).order_by("-item_count")


class TagDetailView(DetailView):
    queryset = Tag.objects.annotate(
        item_count=Count("taggit_taggeditem_items"),
    ).order_by("-item_count")
    template_name = "tag/detail.html"
    context_object_name = "page_obj"


def items_with_tags(request):
    slugs = request.GET.getlist("slug")
    return render(
        request=request,
        template_name="tag/items.html",
        context={"slugs": slugs},
    )
