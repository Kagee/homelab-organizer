from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.views.generic import DetailView

from hlo.filters import OrderItemFilter
from hlo.models import OrderItem


def product_list(request):
    qs_orderitems = (
        OrderItem.objects.exclude(meta__hidden=True)  # Items with meta = hidden
        .select_related("order")
        .select_related("order__shop")
        .prefetch_related("stockitems")
        .order_by("-order__date")
    )
    # .values('id', 'name', 'thumbnail', 'order')
    f = OrderItemFilter(request.GET, queryset=qs_orderitems)
    paginator = Paginator(f.qs, 10)

    page = request.GET.get("page")
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)
    return render(
        request,
        "orderitem/filter.html",
        {"page_obj": response, "filter": f},
    )


class OrderItemDetailView(DetailView):
    model = OrderItem
    template_name = "orderitem/detail.html"
    context_object_name = "order_item"


__all__ = [
    "product_list",
    "OrderItemDetailView",
]
