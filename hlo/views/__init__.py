import logging

from django.contrib import messages
from django.core.cache import cache
from django.shortcuts import redirect, render

from hlo.models import Attachement, OrderItem, StockItem

from .category import *
from .combined_search import *
from .orderitems import *
from .orders import *
from .project import *
from .search import *
from .stockitems import *
from .storage import *

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


def barcode(request, barcode: str):
    oi: OrderItem = OrderItem.objects.filter(gen_id=barcode).first()
    if not oi:
        messages.add_message(
            request,
            messages.WARNING,
            f"Could not find item with barcode {barcode}.",
        )
        return redirect("index")

    if oi.stockitem.count():
        return redirect("stockitem-detail", pk=oi.stockitem.first().pk)
    return redirect("orderitem", pk=oi.pk)


def render404(request, _exception):
    return render(request, "404.html")
