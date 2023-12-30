# No views for HLO project (for now?)

from haystack.generic_views import SearchView # , FacetedSearchView

from haystack.forms import SearchForm
from haystack.query import SearchQuerySet

class JohnSearchView(SearchView):
    template_name = 'search/search.html'
    queryset = SearchQuerySet().all()
    form_class = SearchForm

