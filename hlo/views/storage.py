from django.views.generic import CreateView, DetailView, ListView, UpdateView

from hlo.models import Storage


class StorageDetailView(DetailView):
    model = Storage
    template_name = "storage/detail.html"
    context_object_name = "storage"

class StorageListView(ListView):
    model = Storage
    template_name = "storage/list.html"
    context_object_name = "storages"

class StorageCreateView(CreateView):
    model = Storage
    template_name = "storage/form.html"
    context_object_name = "storage"

class StorageUpdateView(UpdateView):
    model = Storage
    template_name = "storage/form.html"
    context_object_name = "storage"
