import logging
from django.shortcuts import render
from django.db.models import Q
from haystack.generic_views import SearchView
from haystack.forms import SearchForm
from haystack.query import SearchQuerySet

# pylint: disable=wildcard-import,unused-wildcard-import
from hlo.models import *
from hlo.views.orders import *
from hlo.views.orderitems import *
from hlo.views.stockitems import *

logger = logging.getLogger(__name__)


# Create your views here.
def index(request):
    # count stuff here
    # order_count = 0
    return render(
        request, "index.html", {
            "orderitem_count": OrderItem.objects.count(),
            "stockitem_count": StockItem.objects.count(),
            "stockitem_with_location": 0,
            "stockitem_without_location": 0,
            "attachement_count": Attachement.objects.count(),
            "attachement_pdf": Attachement.objects.filter(file__endswith=".pdf").count(),
            "attachement_html": Attachement.objects.filter(file__endswith=".html").count(),
            "order_count": Order.objects.count(),
            }
    )


class JohnSearchView(SearchView):
    template_name = "search/search.html"
    queryset = SearchQuerySet().all()
    form_class = SearchForm
