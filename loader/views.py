import logging
logger = logging.getLogger(__name__)

from django.shortcuts import render


# views.py
from django.views.generic import ListView
from django_filters.views import FilterView
from loader.models import OrderItem
from loader.filters import OrderItemFilter
from django.views.generic.list import MultipleObjectMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def product_list(request):
    f = OrderItemFilter(request.GET, queryset=OrderItem.objects.all())
    paginator = Paginator(f.qs, 2)

    page = request.GET.get('page')
    try:
        response = paginator.page(page)
        logger.error("page: %s", page)
    except PageNotAnInteger:
        logger.error("PageNotAnInteger")
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)
        logger.error("EmptyPage")
    return render(
        request,
        'loader/orderitem_filter.html', 
        {'page_obj': response, 'filter': f}
    )
    #return render(request, 'loader/orderitems_filter.html', {'filter': f})

class OrderItemFilterListView(FilterView): #, MultipleObjectMixin):
    model = OrderItem
    filterset_fields = ['order__shop', 'name']
    paginate_by = 5

class OrderItemListView(ListView):
    model = OrderItem
    context_object_name = "order_items"
    paginate_by = 2