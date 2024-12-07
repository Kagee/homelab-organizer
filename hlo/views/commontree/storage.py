import logging
from typing import Any

from crispy_forms.helper import FormHelper
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from hlo.models import Storage

logger = logging.getLogger(__name__)


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

    def get_success_url(self):
        if (
            "submit" in self.request.POST
            and self.request.POST["submit"] == "view-parent"
        ):
            if self.object.parent:
                return self.object.parent.get_absolute_url()
            return reverse("storage-list")
        return super().get_success_url()

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
    fields = ["name", "name_secondary", "comment", "parent"]

    def get_success_url(self):
        if (
            "submit" in self.request.POST
            and self.request.POST["submit"] == "view-parent"
        ) and self.object.parent:
            return self.object.parent.get_absolute_url()
        return super().get_success_url()

    def get_form(self, form_class=None):
        # Should be moved to modelform?
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.form_method = "post"
        form.helper.form_class = "form-horizontal"
        form.helper.label_class = "col-2"
        form.helper.field_class = "col-10"
        return form
