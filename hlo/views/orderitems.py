from django.shortcuts import render
from django.views.generic import DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from hlo.models import OrderItem
from hlo.filters import OrderItemFilter


def product_list(request):
    f = OrderItemFilter(request.GET, queryset=OrderItem.objects.all().order_by('-order__date'))
    paginator = Paginator(f.qs, 10)

    page = request.GET.get('page')
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)
    return render(
        request,
        'orderitem/filter.html',
        {'page_obj': response, 'filter': f}
    )

class OrderItemDetailView(DetailView):
    model = OrderItem
    template_name = "orderitem/detail.html"
    context_object_name = "order_item"
