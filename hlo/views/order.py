import logging

from crispy_forms.layout import (
    Submit,
)
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from hlo.forms import OrderAttachementInlineFormSet, OrderForm, OrderFormSimple

# pylint: disable=wildcard-import,unused-wildcard-import
from hlo.models import Order, Shop

logger = logging.getLogger(__name__)


class OrderListView(ListView):
    model = Order
    template_name = "order/list.html"


class OrderDetailView(DetailView):
    model = Order
    template_name = "order/detail.html"


class OrderSimpleCreateView(CreateView):
    model = Order
    template_name = "order/formset.html"
    form_class = OrderFormSimple

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formset"] = OrderAttachementInlineFormSet()
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["shop"].initial = Shop.objects.get(
            pk=self.kwargs["shop"],
        )
        return form

    def post(self, request, *_args, **_kwargs):
        formset = OrderAttachementInlineFormSet(request.POST)
        form = OrderFormSimple(request.POST)
        if formset.is_valid() and form.is_valid():
            return self.form_valid(formset, form)
        return self.form_invalid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, formset, form):
        self.object = form.save()
        instances = formset.save(commit=False)
        for instance in instances:
            self.object.attachements.add(instance)
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


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
