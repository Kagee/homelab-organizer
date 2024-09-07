import logging
from typing import Any

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
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.forms.widgets import Select
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, DetailView, UpdateView
from django_select2.views import AutoResponseView
from openai import OpenAI

from hlo.filters import StockItemFilter
from hlo.forms import StockItemForm
from hlo.models import OrderItem, OrderItemMeta, StockItem

logger = logging.getLogger(__name__)


class TagAutoResponseView(AutoResponseView):
    def get(self, request, *_args, **kwargs):
        """This method is overriden for changing id to name instead of pk."""
        # pylint: disable=attribute-defined-outside-init
        self.widget = self.get_widget_or_404()
        self.term = kwargs.get("term", request.GET.get("term", ""))
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return JsonResponse(
            {
                "results": [
                    {
                        "text": self.widget.label_from_instance(obj),
                        "id": obj.name,
                    }
                    for obj in context["object_list"]
                ],
                "more": context["page_obj"].has_next(),
            },
        )


class StockItemCreate(CreateView):
    model = StockItem
    template_name = "stockitem/form.html"
    form_class = StockItemForm

    def get_ai_name_from_orderitem(self, oi: OrderItem) -> str | None:
        if not settings.OPENAPI_PROJECT_API_KEY:
            return None
        if hasattr(oi, "meta") and oi.meta.ai_name:
            return oi.meta.ai_name

        query = settings.OPENAPI_TITLE_CLEANUP_QUERY.format(
            title=oi.name,
        )
        client = OpenAI(
            api_key=settings.OPENAPI_PROJECT_API_KEY,
        )
        result = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": query,
                },
            ],
            model=settings.OPENAPI_TITLE_CLEANUP_MODEL,
        )
        ai_name = result.choices[0].message.content.strip('"')
        oim, created = OrderItemMeta.objects.get_or_create(parent=oi)
        oim.ai_name = ai_name
        oim.save()
        return ai_name

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Create stock item"
        if "fromitems" in self.kwargs:
            oi = get_object_or_404(
                OrderItem.objects.prefetch_related("meta"),
                pk=int(self.kwargs["fromitems"].split(",")[0]),
            )
            ai_name = oi.name
            name_help = "Original name from order"
            if title := self.get_ai_name_from_orderitem(oi):
                ai_name = title
                name_help = (
                    f"Title as suggested by OpenAIs "
                    f"{settings.OPENAPI_TITLE_CLEANUP_MODEL}"
                )

            ctx["original_name"] = oi.name
            ctx["orderitem"] = oi
            ctx["ai_name"] = ai_name
            form = ctx["form"]
            form.fields["name"].initial = ai_name
            form.fields["name"].help_text = name_help

        return ctx

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # if get paramenter fromitems is set, lock down orderitem list
        if "fromitems" in self.kwargs:
            form.fields["orderitems"].label = "Order items"
            form.fields["orderitems"].disabled = True
            form.fields["orderitems"].queryset = OrderItem.objects.filter(
                pk__in=[int(x) for x in self.kwargs["fromitems"].split(",")],
            )
            # Grow/shrink the html list size as required
            form.fields["orderitems"].widget.attrs["size"] = min(
                form.fields["orderitems"].queryset.all().count(),
                5,
            )
        return form

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super().get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        # if get paramenter fromitems is set, preselect these items
        if "fromitems" in self.kwargs:
            qs = OrderItem.objects.filter(
                pk__in=[int(x) for x in self.kwargs["fromitems"].split(",")],
            )
            initial["orderitems"] = qs
        return initial


class StockItemUpdate(UpdateView):
    model = StockItem
    template_name = "stockitem/form.html"
    context_object_name = "stockitem"
    form_class = StockItemForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["initial_tags"] = [
            (x["name"], x["name"]) for x in self.object.tags.all().values()
        ]
        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields["count_unit"].widget = Select(
            choices=[
                (x["count_unit"], x["count_unit"])
                for x in StockItem.objects.order_by()
                .values("count_unit")
                .distinct()
            ],
        )

        # if get paramenter fromitems is set, lock down orderitem list
        if oi := self.object.orderitems.first().pk:
            form.fields["orderitems"].label = "Order items"
            form.fields["orderitems"].disabled = True
            form.fields["orderitems"].queryset = OrderItem.objects.filter(
                pk=oi,
            )
            form.fields["orderitems"].widget.attrs["size"] = 1
        return form

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx["image_tag"] = ctx["object"].thumbnail_url
        ctx["title"] = "Update stock item"
        return ctx


class StockItemDetail(DetailView):
    model = StockItem
    queryset = model.objects.all().prefetch_related(
        "tags",
        "orderitems",
    )
    template_name = "stockitem/detail.html"
    context_object_name = "stockitem"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx["range"] = list(range(13))
        return ctx


def stockitem_list(request):
    qs_stockitems = StockItem.objects.all()

    f = StockItemFilter(request.GET, queryset=qs_stockitems)
    paginator = Paginator(f.qs, 10)

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
                        {"style": "width: 30%; display: inline-block;"},
                        {"style": "width: 70%; display: inline-block;"},
                    ),
                    wrapper_class="hemmelig",
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

    page = request.GET.get("page")
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)
    return render(
        request,
        "stockitem/filter.html",
        {
            "page_obj": response,
            "filter": f,
        },
    )
