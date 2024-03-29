import logging

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, UpdateView
from django_select2 import forms as s2forms
from django_select2.forms import ModelSelect2TagWidget
from django_select2.views import AutoResponseView
from taggit.models import Tag

from hlo.filters import StockItemFilter
from hlo.models import OrderItem, StockItem

logger = logging.getLogger(__name__)


class TagAutoResponseView(AutoResponseView):
    def get(self, request, *_args, **kwargs):
        """This method is overriden for changing id to name instead of pk.
        """
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


class TagChoices(ModelSelect2TagWidget):
    queryset = Tag.objects.all().order_by("name")
    search_fields = ["name__icontains"]
    empty_label = "Start typing to search or create tags..."

    def get_model_field_values(self, value) -> dict:
        return {"name": value}

    def value_from_datadict(self, data, files, name):
        """Create objects for missing tags.

        Return comma separates string of tags.
        """
        values = set(super().value_from_datadict(data, files, name))
        names = self.queryset.filter(name__in=list(values)).values_list(
            "name",
            flat=True,
        )
        names = set(map(str, names))
        cleaned_values = list(names)
        # if a value is not in names (tag with name does
        # not exists), it has to be created
        cleaned_values += [
            self.queryset.create(name=val).name
            for val in (values - names)
            ]
        # django-taggit expects a comma-separated list
        return ",".join(cleaned_values)


class ExampleForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)


class StockItemCreate(CreateView):
    model = StockItem
    template_name = "stockitem/form.html"
    fields = ["name", "count", "tags", "orderitems"]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # django-crispy-form formhelper
        # https://django-crispy-forms.readthedocs.io/en/latest/form_helper.html
        form.helper = FormHelper()
        form.helper.add_input(
            Submit("submit", "Create", css_class="btn-primary"),
        )
        # We override the widget for tags for autocomplete
        form.fields["tags"].widget = TagChoices(
            data_view="stockitem-tag-auto-json",
        )

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
            #
            logger.error(dir(form.fields["name"]))  # .value = "Order items"
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
            initial["name"] = qs.first().name
        return initial


class StockItemDetail(DetailView):
    model = StockItem
    queryset = model.objects.all().prefetch_related(
        "tags",
        "orderitems",
    )
    template_name = "stockitem/detail.html"
    context_object_name = "stockitem"


class CommonTreeWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "name__icontains",
    ]


class StockItemUpdate(UpdateView):
    model = StockItem
    template_name = "stockitem/form.html"
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

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # We override the widget for tags for autocomplete
        form.fields["tags"].widget = TagChoices()
        # if get paramenter fromitems is set, lock down orderitem list
        return form


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
