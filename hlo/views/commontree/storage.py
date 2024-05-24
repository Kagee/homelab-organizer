from typing import Any

from crispy_forms.helper import FormHelper
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from hlo.models import Storage


class StorageCreateView(CreateView):
    model = Storage
    template_name = "storage/form.html"
    context_object_name = "storage"
    fields = ["name", "name_secondary", "comment", "parent"]

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super().get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        # if get paramenter parent is set, preselect these items
        if "parent" in self.kwargs:
            obj = Storage.objects.get(
                pk=self.kwargs["parent"],
            )
            initial["parent"] = obj
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # django-crispy-form formhelper
        # https://django-crispy-forms.readthedocs.io/en/latest/form_helper.html

        form.helper = FormHelper()
        form.helper.form_method = "post"
        form.helper.form_class = "form-horizontal"
        form.helper.label_class = "col-2"
        form.helper.field_class = "col-10"
        return form


class StorageDetailView(DetailView):
    model = Storage
    template_name = "storage/detail.html"
    context_object_name = "storage"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)

        ctx["packaging"] = ctx["storage"].comment.split("\n")[0].strip()

        return ctx


class StorageListView(ListView):
    model = Storage
    template_name = "storage/list.html"
    context_object_name = "storages"


class StorageUpdateView(UpdateView):
    model = Storage
    template_name = "storage/form.html"
    context_object_name = "storage"
