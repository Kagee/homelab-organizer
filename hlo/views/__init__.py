import logging
from django.shortcuts import render
from haystack.generic_views import SearchView # , FacetedSearchView
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
    #order_count = 0
    return render(request, "index.html", {'order_count': 0})

class JohnSearchView(SearchView):
    template_name = 'search/search.html'
    queryset = SearchQuerySet().all()
    form_class = SearchForm
