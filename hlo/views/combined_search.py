import logging

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    HTML,
    ButtonHolder,
    Column,
    Layout,
    MultiWidgetField,
    Row,
    Submit,
)
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.views.generic import DetailView

from hlo.filters import OrderItemFilter, StockItemFilter
from hlo.models import OrderItem, StockItem

logger = logging.getLogger(__name__)


def item_search(request):
    qs_orderitems = (
        OrderItem.objects.exclude(meta__hidden=True)  # Items with meta = hidden
        .select_related("order")
        .select_related("order__shop")
        .prefetch_related("stockitems")
        .order_by("-order__date")
    )
    f_orderitems = OrderItemFilter(request.GET, queryset=qs_orderitems)

    # <QueryDict: {
    # 'name': ['aname'],
    # 'name_lookup': ['icontains'],
    # 'date_range': ['month'],
    # 'shop': ['7'],
    # 'ordering': ['order__date']}> // -order__date
    # orderitem__order__date
    # -orderitem__order__date
    # tempdict = request.GET.copy()
    # tempdict['state'] = ['XYZ',]
    # tempdict['ajaxtype'] = ['facet',]
    # self.request.GET = tempdict  # this is the added line

    request_get_copy = request.GET.dict()
    if "ordering" in request.GET and request.GET["ordering"] in [
        "order__date",
        "-order__date",
    ]:
        request_get_copy["ordering"] = {
            "order__date": "orderitem__order__date",
            "-order__date": "-orderitem__order__date",
        }[request_get_copy["ordering"]]

    qs_stockitems = StockItem.objects.all()
    f_stockitems = StockItemFilter(request_get_copy, queryset=qs_stockitems)

    logger.info("Stockitems: %s", f_stockitems.qs.count())

    all_orderitems = []

    for stockitem in f_stockitems.qs:
        # stockitem.orderitem is m2m
        for order_stock_item_link in stockitem.orderitem.all():
            logger.info("Orderitem.pk=%s", order_stock_item_link.orderitem.pk)

            all_orderitems.append(order_stock_item_link.orderitem)

    logger.info("Orderitems: %s", f_orderitems.qs.count())
    for orderitem in f_orderitems.qs:
        if orderitem in all_orderitems:
            logger.info(
                "Already found via stockitem Orderitem.pk=%s", orderitem.pk
            )
        else:
            logger.info("New Orderitem.pk=%s", orderitem.pk)

    """
    [I] Stockitems: 2
    [I] Orderitem.pk=3684
    [I] Orderitem.pk=3783
    
    [I] Orderitems: 3
    [I] Already found via stockitem Orderitem.pk=3783
    [I] Already found via stockitem Orderitem.pk=3684
    [I] New Orderitem.pk=3681
    """

    return render(
        request,
        "search/items.html",
        {
            "filter_oi": f_orderitems,
            "filter_si": f_stockitems,
            "get_values": request.GET,
            "get_values_copy": request_get_copy,
        },
    )


__all__ = [
    "item_search",
]
