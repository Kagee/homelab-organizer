import logging

from crispy_forms.layout import (
    Submit,
)
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from hlo.forms import OrderForm

# pylint: disable=wildcard-import,unused-wildcard-import
from hlo.models import Order, Shop

logger = logging.getLogger(__name__)


class OrderListView(ListView):
    model = Order
    template_name = "order/list.html"


class OrderDetailView(DetailView):
    model = Order
    template_name = "order/detail.html"


class OrderCreateView(CreateView):
    model = Order
    template_name = "order/form.html"
    form_class = OrderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create new Order object"
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper.add_input(Submit("submit", "Create Order object"))
        # if get paramenter fromitems is set, lock down orderitem list
        if "shop" in self.kwargs:
            form.fields["shop"].disabled = True
            form.fields["shop"].initial = Shop.objects.get(
                pk=self.kwargs["shop"],
            )
        return form


class OrderUpdateView(UpdateView):
    model = Order
    template_name = "order/form.html"
    form_class = OrderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = (
            f"Update {context['order'].shop.branch_name}#{context['order'].order_id}"
        )
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        if not self.object.manual_input:
            for field in form.fields.values():
                field.widget.attrs["disabled"] = "disabled"
            form.helper.add_input(
                Submit("submit", "Update Order object", disabled="disabled"),
            )
        else:
            form.helper.add_input(Submit("submit", "Update Order object"))
        return form
