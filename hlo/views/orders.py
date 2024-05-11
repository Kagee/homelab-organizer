from django.views.generic import CreateView, DetailView, ListView, UpdateView

# pylint: disable=wildcard-import,unused-wildcard-import
from hlo.models import Order


class OrderListView(ListView):
    model = Order
    template_name = "order/list.html"


class OrderDetailView(DetailView):
    model = Order
    template_name = "order/detail.html"


class OrderCreateView(CreateView):
    model = Order
    template_name = "order/form.html"


class OrderUpdateView(UpdateView):
    model = Order
    template_name = "order/form.html"
