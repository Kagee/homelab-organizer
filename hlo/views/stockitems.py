from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

from django_select2.forms import ModelSelect2TagWidget
from django_select2.views import AutoResponseView

from taggit.models import Tag

from hlo.models import StockItem
from hlo.filters import StockItemFilter


class TagAutoResponseView(AutoResponseView):
    def get(self, request, *args, **kwargs):
        """
        This method is overriden for changing id to name instead of pk.
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
            }
        )


class TagChoices(ModelSelect2TagWidget):
    queryset = Tag.objects.all().order_by("name")
    search_fields = ["name__icontains"]
    empty_label = "Start typing to search or create tags..."

    def get_model_field_values(self, value):
        return {"name": value}

    def value_from_datadict(self, data, files, name):
        """Create objects for missing tags. Return comma separates string of tags."""
        values = set(super().value_from_datadict(data, files, name))
        names = self.queryset.filter(**{"name__in": list(values)}).values_list(
            "name", flat=True
        )
        names = set(map(str, names))
        cleaned_values = list(names)
        # if a value is not in names (tag with name does not exists), it has to be created
        for val in values - names:
            cleaned_values.append(self.queryset.create(name=val).name)
        # django-taggit expects a comma-separated list
        return ",".join(cleaned_values)


class StockItemCreate(CreateView):
    model = StockItem
    template_name = "stockitem/form.html"
    fields = ["name", "count", "tags", "orderitems"]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # We override the widget for tags for autocomplete
        form.fields["tags"].widget = TagChoices(
            data_view="stockitem-tag-auto-json"
        )

        # if get paramenter fromitems is set, lock down orderitem list
        if "fromitems" in self.kwargs:
            form.fields["orderitems"].label = "Order items"
            form.fields["orderitems"].disabled = True
            form.fields["orderitems"].queryset = OrderItem.objects.filter(
                pk__in=[int(x) for x in self.kwargs["fromitems"].split(",")]
            )
            # Grow/shrink the html list size as required
            form.fields["orderitems"].widget.attrs["size"] = min(
                form.fields["orderitems"].queryset.all().count(), 5
            )
        return form

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super().get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        # if get paramenter fromitems is set, preselect these items
        if "fromitems" in self.kwargs:
            initial["orderitems"] = OrderItem.objects.filter(
                pk__in=[int(x) for x in self.kwargs["fromitems"].split(",")]
            )
        return initial


class StockItemDetail(DetailView):
    model = StockItem
    template_name = "stockitem/detail.html"
    context_object_name = "stock_item"


class StockItemUpdate(UpdateView):
    model = StockItem
    template_name = "stockitem/form.html"
    context_object_name = "stock_item"
    fields = ["name", "count", "tags", "orderitems"]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # We override the widget for tags for autocomplete
        form.fields["tags"].widget = TagChoices()
        # if get paramenter fromitems is set, lock down orderitem list
        return form


def stockitem_list(request):
    qs_orderitems = (
        StockItem.objects.all()
    )
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
        request, "stockitem/filter.html", {"stockitems": response, "filter": f}
    )
