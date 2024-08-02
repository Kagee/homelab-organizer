from haystack.forms import SearchForm
from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet


class AttachmentSearchView(SearchView):
    template_name = "search/search.html"
    queryset = SearchQuerySet().all()
    form_class = SearchForm
