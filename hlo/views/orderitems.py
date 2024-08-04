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
from django import forms
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, UpdateView

from hlo.filters import OrderItemFilter
from hlo.forms import OrderItemForm
from hlo.models import Order, OrderItem

logger = logging.getLogger(__name__)


def orderitem_filtered_list(
    request: WSGIRequest,
) -> HttpResponse:
    qs_orderitems = (
        OrderItem.objects.exclude(meta__hidden=True)  # Items with meta = hidden
        .exclude(stockitems__count__gt=0)
        .select_related("order")
        .select_related("order__shop")
        .prefetch_related("stockitems")
        .order_by("-order__date", "name")
    )
    per_page_choices = [5, 10, 20, 50, 100]
    # per_page_choices = [(5, 5), (10, 10), (20, 20), (50, 50), (100, 100)]
    per_page = 10
    if "per_page" in request.GET:
        per_page = int(request.GET["per_page"])
        if per_page not in per_page_choices:
            per_page_choices.append(per_page)

    f = OrderItemFilter(request.GET, queryset=qs_orderitems)
    paginator = Paginator(f.qs, per_page)

    f.form.fields["per_page"] = forms.fields.ChoiceField(
        choices=[(choice, choice) for choice in per_page_choices],
    )
    logger.debug(f.form.fields["name"].widget.widgets[1])
    # Swap the name and render order for the name fields
    f.form.fields["name"].widget.suffixes = ["lookup", None]
    f.form.fields["name"].widget.widgets = (
        forms.widgets.HiddenInput(),
        f.form.fields["name"].widget.widgets[0],
    )

    f.form.helper = FormHelper()
    f.form.helper.form_method = "get"
    f.form.helper.form_class = "align-items-bottom"
    f.form.helper.form_style = "inline"
    f.form.helper.form_show_labels = True
    f.form.helper.label_class = "fs-6"
    layout = Layout(
        Row(
            Column(
                MultiWidgetField(
                    "name",
                    attrs=(
                        {},  # hidden
                        {"style": "display: inline-block;"},
                    ),
                ),
                css_class="col-4",
            ),
            *[
                Column(field, css_class="col")
                for field in f.form.fields
                if field != "name"  # and field != "per_page"
            ],
            Column(
                ButtonHolder(
                    HTML(
                        '<a href="{{ request.path }}" '
                        'class="btn btn-secondary col ">Clear</a>',
                    ),
                    Submit("submit", "Submit", css_class="btn btn-primary col"),
                    css_class="row align-items-end h-100 pb-3",
                ),
                css_class="col",
            ),
            css_class="pt-3",
        ),
    )
    f.form.helper.add_layout(layout)

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
    queryset = (
        OrderItem.objects.select_related("meta")
        .select_related("order")
        .select_related("order__shop")
    )
    template_name = "orderitem/detail.html"


class OrderItemCreateView(CreateView):
    model = OrderItem
    template_name = "orderitem/form.html"
    form_class = OrderItemForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create new order item object"
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper.add_input(Submit("submit", "Create order item object"))
        # if get parameter fromitems is set, lock down orderitem list
        if "order" in self.kwargs:
            form.fields["order"].disabled = True
            form.fields["order"].initial = Order.objects.get(
                pk=self.kwargs["order"],
            )
        return form


class OrderItemUpdateView(UpdateView):
    model = OrderItem
    template_name = "orderitem/form.html"
    form_class = OrderItemForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update item"
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        if not self.object.manual_input:
            for field in form.fields.values():
                field.disabled = "disabled"
            form.helper.add_input(
                Submit(
                    "submit",
                    "Update item object",
                    disabled="disabled",
                ),
            )
        else:
            form.helper.add_input(Submit("submit", "Update item object"))
        return form


__all__ = [
    "orderitem_filtered_list",
    "OrderItemDetailView",
    "OrderItemCreateView",
    "OrderItemUpdateView",
]
