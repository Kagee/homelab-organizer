# ruff: noqa: ERA001,N806
import logging

from crispy_forms.helper import FormHelper  # type: ignore[import-untyped]
from crispy_forms.layout import (  # type: ignore[import-untyped]
    HTML,
    ButtonHolder,
    Column,
    Field,
    Layout,
    Row,
    Submit,
)
from django import forms
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, DetailView, UpdateView

from hlo.filters import OrderItemFilter
from hlo.forms import OrderItemForm
from hlo.models import Order, OrderItem, OrderItemMeta

logger = logging.getLogger(__name__)


def orderitem_filtered_list(
    request: WSGIRequest,
) -> HttpResponse:
    qs_orderitems = (
        OrderItem.objects.select_related("order")
        .select_related("order__shop")
        .prefetch_related("stockitems")
        .order_by("-order__date")
    )
    per_page_choices = [5, 10, 20, 50, 100]
    per_page = 15
    if "per_page" in request.GET:
        per_page = int(request.GET["per_page"])
        #  May be random value calculated by JS
        if per_page not in per_page_choices:
            per_page_choices.append(per_page)

    f = OrderItemFilter(request.GET, queryset=qs_orderitems)
    paginator = Paginator(f.qs, per_page)

    f.form.fields["per_page"] = forms.fields.ChoiceField(
        choices=[(choice, choice) for choice in per_page_choices],
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
                Field(
                    "name",
                ),
                css_class="col-4",
            ),
            *[
                Column(field, css_class="col")
                for field in f.form.fields
                if field != "name"
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

    page = request.GET.get("page") or 1

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


@require_http_methods(["POST"])
def orderitem_hide(request, pk: int, hide: str):
    if hide not in ("true", "false"):
        return JsonResponse(
            {"message": f"Hide value must be true/false, was {hide}"},
            status=400,
        )
    obj = OrderItem.objects.filter(pk=pk).first()
    if not obj:
        return JsonResponse(
            {"message": f"No OrderItem with pk {pk} found"},
            status=400,
        )
    # For some odd reason, possibly because we are using a on2on on a specific
    # field,get_or_create does not work
    if not hasattr(obj, "meta"):
        obj_meta = OrderItemMeta.objects.create(parent=obj)
    else:
        obj_meta = obj.meta
    if "comment" in request.POST:
        obj_meta.comment = request.POST["comment"]
    obj_meta.hidden = hide == "true"
    obj_meta.save()
    return JsonResponse({"message": "OK"}, status=200)


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
