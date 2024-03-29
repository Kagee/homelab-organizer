from django.views.generic import CreateView, DetailView, ListView, UpdateView

from hlo.models import Category


class CategoryCreateView(CreateView):
    model = Category
    template_name = "category/form.html"
    context_object_name = "category"


class CategoryDetailView(DetailView):
    model = Category
    template_name = "category/detail.html"
    context_object_name = "category"


class CategoryListView(ListView):
    model = Category
    template_name = "category/list.html"
    context_object_name = "categories"


class CategoryUpdateView(UpdateView):
    model = Category
    template_name = "category/form.html"
    context_object_name = "category"


__all__ = [
    "CategoryCreateView",
    "CategoryDetailView",
    "CategoryListView",
    "CategoryUpdateView",
]
