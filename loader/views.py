from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from loader.models import OrderItem, Order
from loader.filters import OrderItemFilter


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
        'loader/orderitem_filter.html',
        {'page_obj': response, 'filter': f}
    )

#class OrderItemListView(ListView):
#    model = OrderItem
#    context_object_name = "order_items"
#    order_by = ""
#    paginate_by = 20

class OrderItemDetailView(DetailView):
    model = OrderItem
    context_object_name = "order_item"


class OrderListView(ListView):
    model = Order
    #context_object_name = "order" #object_list

class OrderDetailView(DetailView):
    model = Order
    # context_object_name = "order" #object
