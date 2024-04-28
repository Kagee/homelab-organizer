import logging

from django.db.models import Count, F
from django.shortcuts import render

from hlo.filters import NonOrderingOrderItemFilter, NonOrderingStockItemFilter
from hlo.models import OrderItem, StockItem

logger = logging.getLogger(__name__)


def item_search(request):
    qs_orderitems = (
        OrderItem.objects.all()
        .exclude(meta__hidden=True)  # Items with meta = hidden
        .select_related("order")
        .select_related("order__shop")
        .prefetch_related("stockitems")
        .order_by()
    )
    f_orderitems = NonOrderingOrderItemFilter(
        request.GET,
        queryset=qs_orderitems,
    )

    qs_stockitems = (
        StockItem.objects.all()
        .select_related("orderitem__order")
        .select_related("orderitem__order__shop")
        .prefetch_related("orderitems")
        .order_by()
    )
    f_stockitems = NonOrderingStockItemFilter(
        request.GET,
        queryset=qs_stockitems,
    )

    orderitems_from_stockitems = (
        OrderItem.objects.filter(
            stockitem__in=f_stockitems.qs.values("orderitem"),
        )
        .exclude(meta__hidden=True)  # Items with meta = hidden
        .select_related("order")
        .select_related("order__shop")
        .prefetch_related("stockitems")
        .annotate(stockitem_count=Count("stockitem"))
        .annotate(stockitem_name=F("stockitem__stockitem__name"))
        .order_by()
    )

    orderitems = (
        f_orderitems.qs.exclude(orderitem__in=orderitems_from_stockitems)
        .annotate(stockitem_count=Count("stockitem"))
        .annotate(stockitem_name=F("stockitem__stockitem__name"))
        .union(orderitems_from_stockitems)
        .order_by(
            "-stockitem_count",
            "stockitem_name",
            "name",
        )
    )

    return render(
        request,
        "search/items.html",
        {
            # both orderitem and stockitem search
            # use the same form input names,
            # so we only need one form
            "combined_form": f_orderitems.form,
            "orderitems": orderitems,
        },
    )


__all__ = [
    "item_search",
]
