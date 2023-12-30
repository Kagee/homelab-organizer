import logging
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import StockItem
from loader.models import OrderItem

logger = logging.getLogger(__name__)


# Create your views here.
def index(request):
    return render(request, template_name="inventory/index.html")


class StockItemCreate(CreateView):
    model = StockItem
    fields = ["name", "count", "tags", "orderitems", "attachements"]

    def get_form(self, form_class=None):
        f = super().get_form(form_class)
        if "id_orderitems" in self.kwargs:
            f.fields["orderitems"].label = "Preselected order items"
            f.fields["orderitems"].disabled = True
            f.fields["orderitems"].queryset = OrderItem.objects.filter(
                pk__in=[int(x) for x in self.kwargs["id_orderitems"].split(",")]
            )
            f.fields["orderitems"].widget.attrs["size"] = min(
                f.fields["orderitems"].queryset.all().count(), 5
            )
        # Try to use this for tags: https://django-select2.readthedocs.io/en/latest/
        # or this https://stackoverflow.com/questions/18743253/manage-tag-with-django-select2
        return f

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super().get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        if "id_orderitems" in self.kwargs:
            initial["orderitems"] = OrderItem.objects.filter(
                pk__in=[int(x) for x in self.kwargs["id_orderitems"].split(",")]
            )
        return initial


class StockItemDetail(DetailView):
    model = StockItem
    context_object_name = "stock_item"


class StockItemList(ListView):
    model = StockItem
    context_object_name = "stock_items"
    paginate_by = 20
