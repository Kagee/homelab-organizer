import logging

from crispy_forms.layout import (
    Submit,
)
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.shortcuts import render

from hlo.forms import ShopForm

# pylint: disable=wildcard-import,unused-wildcard-import
from hlo.models import Order, Shop

logger = logging.getLogger(__name__)


class ShopListView(PermissionRequiredMixin, ListView):
    model = Shop
    template_name = "shop/list.html"
    context_object_name = "shops"
    permission_required = ["hlo.view_shop"]

    #def handle_no_permission(self):
    #    logger.debug("no permission")
    #    return render(self.request, "common/no_access.html")

    #def get_permission_denied_message(self):
    #    return "Fuck off"


class ShopDetailView(PermissionRequiredMixin, DetailView):
    model = Shop
    template_name = "shop/detail.html"
    context_object_name = "shop"
    permission_required = ["hlo.view_shop"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["orders"] = Order.objects.filter(shop=context["object"])
        return context


class ShopCreateView(PermissionRequiredMixin, CreateView):
    model = Shop
    template_name = "shop/form.html"
    context_object_name = "shop"
    form_class = ShopForm
    permission_required = ["hlo.add_shop"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create new shop object"
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper.add_input(Submit("submit", "Create Shop object"))
        return form


class ShopUpdateView(PermissionRequiredMixin, UpdateView):
    model = Shop
    template_name = "shop/form.html"
    context_object_name = "shop"
    form_class = ShopForm
    permission_required = ["hlo.change_shop"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Update {context['shop'].name}"
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        if not self.object.manual_input:
            for field in form.fields.values():
                field.widget.attrs["disabled"] = "disabled"
            form.helper.add_input(
                Submit("submit", "Update Shop object", disabled="disabled"),
            )
        else:
            form.helper.add_input(Submit("submit", "Update Shop object"))
        return form
