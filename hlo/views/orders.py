from django.views.generic import DetailView, ListView

# pylint: disable=wildcard-import,unused-wildcard-import
from hlo.models import Order


class OrderListView(ListView):
    model = Order
    template_name = "order/list.html"
    #context_object_name = "order" #object_list  # noqa: ERA001

class OrderDetailView(DetailView):
    model = Order
    template_name = "order/detail.html"
    # context_object_name = "order" #object  # noqa: ERA001
