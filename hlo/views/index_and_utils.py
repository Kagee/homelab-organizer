import logging

from django.apps import apps
from django.core.cache import cache
from django.db.models import Q
from django.shortcuts import render

from hlo.models import Attachment, OrderItem, StockItem

logger = logging.getLogger(__name__)

# To clear a key somewhere else:
# cache.delete_many([...],)
INDEX_DATA_CACHE_KEYS: dict = {  # type: ignore[annotation-unchecked]
    "orderitem_raw_count": OrderItem.objects.count,
    "orderitem_unprocessed_count": OrderItem.objects.filter(
        Q(stockitems__isnull=True)
        & (
            Q(meta__isnull=True)
            | (Q(meta__isnull=False) & Q(meta__hidden=False))
        ),
    )
    .distinct()
    .count,
    "orderitem_hidden_count": OrderItem.objects.filter(
        Q(meta__isnull=False) & Q(meta__hidden=True),
    )
    .distinct()
    .count,
    "orderitem_processed_count": OrderItem.objects.filter(
        stockitems__isnull=False,
    )
    # if not orderitems with multiple stockitems
    # will be counted more than once
    .distinct()
    .count,
    # STOCKITEMS
    "stockitem_count": StockItem.objects.count,
    # ATTACHMENTS
    "attachment_count": Attachment.objects.count,
    "attachment_pdf": Attachment.objects.filter(
        file__endswith=".pdf",
    ).count,
    "attachment_html": Attachment.objects.filter(
        file__endswith=".html",
    ).count,
}


def index(request):
    # This is basically a suboptimal implementation of a
    # (currently non-existing)cache.get_or_set_many
    # with callable support
    cached_keys = cache.get_many(INDEX_DATA_CACHE_KEYS.keys())
    cache_buster = "bust_cache" in request.GET
    if cache_buster:
        logger.debug("Busting index cache")
    for key in INDEX_DATA_CACHE_KEYS:
        if key not in cached_keys or cache_buster:
            value = INDEX_DATA_CACHE_KEYS[key]()
            cache.set(key, value, timeout=None)
            cached_keys[key] = str(value) + "*"

    return render(
        request,
        "common/index.html",
        cached_keys,
    )


def no_access(request):
    return render(request, "no_access.html")


def render404(request, _exception):
    return render(request, "404.html")
