import logging
from typing import Any

from crispy_forms.helper import FormHelper
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
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
    """
    fields = [
        "name",
        "count",
        "tags",
        "orderitems",
        "category",
        "project",
        "storage",
    ]
    """
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
            ctx["ai_name"] = ai_name
            ctx["image_tag"] = oi.image_tag(0, 300)
            form = ctx["form"]
            form.fields["name"].initial = ai_name
            form.fields["name"].help_text = name_help

        return ctx

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # django-crispy-form formhelper
        # https://django-crispy-forms.readthedocs.io/en/latest/form_helper.html

        form.helper = FormHelper()
        form.helper.form_method = "post"
        form.helper.form_class = "form-horizontal"
        form.helper.label_class = "col-2"
        form.helper.field_class = "col-10"

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


class StockItemDetail(DetailView):
    model = StockItem
    queryset = model.objects.all().prefetch_related(
        "tags",
        "orderitems",
    )
    template_name = "stockitem/detail.html"
    context_object_name = "stockitem"


class StockItemUpdate(UpdateView):
    model = StockItem
    template_name = "stockitem/form2.html"
    context_object_name = "stock_item"
    fields = [
        "name",
        "count",
        "tags",
        "orderitems",
        "attachements",
        "category",
        "project",
        "storage",
    ]


def stockitem_list(request):
    qs_orderitems = StockItem.objects.all()
    f = StockItemFilter(request.GET, queryset=qs_orderitems)
    paginator = Paginator(f.qs, 10)

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
        {"stockitems": response, "filter": f},
    )
