from django.views.generic import CreateView, DetailView, ListView, UpdateView

# pylint: disable=wildcard-import,unused-wildcard-import
from hlo.models import Shop


class ShopListView(ListView):
    model = Shop
    template_name = "shop/list.html"
    context_object_name = "shops"


class ShopDetailView(DetailView):
    model = Shop
    template_name = "shop/detail.html"
    context_object_name = "shop"


class ShopCreateView(CreateView):
    model = Shop
    template_name = "shop/form.html"
    context_object_name = "shop"


class ShopUpdateView(UpdateView):
    model = Shop
    template_name = "shop/form.html"
    context_object_name = "shop"
