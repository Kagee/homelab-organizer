import logging

from django.core.cache import cache
from django.shortcuts import render

from hlo.models import Attachement, OrderItem, StockItem

logger = logging.getLogger(__name__)


def index(request):
    # This is basicly a suboptimal implementation of a (currently non-exsisting)
    # cache.get_or_set_many with callable support
    keys: dict = {
        "orderitem_count": OrderItem.objects.count,
        "stockitem_count": StockItem.objects.count,
        "stockitem_with_location": lambda: 0,
        "stockitem_without_location": lambda: 0,
        "attachement_count": Attachement.objects.count,
        "attachement_pdf": Attachement.objects.filter(
            file__endswith=".pdf",
        ).count,
        "attachement_html": Attachement.objects.filter(
            file__endswith=".html",
        ).count,
    }

    cached_keys = cache.get_many(keys.keys())

    for key in keys:
        if key not in cached_keys:
            value = keys[key]()
            cache.set(key, value, timeout=None)
            cached_keys[key] = value

    return render(
        request,
        "index.html",
        cached_keys,
    )


def render404(request, _exception):
    return render(request, "404.html")
