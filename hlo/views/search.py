from haystack.generic_views import SearchView
from haystack.forms import SearchForm
from haystack.query import SearchQuerySet

class AttachementSearchView(SearchView):
    template_name = "search/search.html"
    queryset = SearchQuerySet().all()
    form_class = SearchForm
