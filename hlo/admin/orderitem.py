from django.contrib import admin
from django.db import models
from django.forms import Textarea, TextInput

from hlo.models import OrderItem


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    search_fields = [
        "name",
        "item_id",
        "item_variation",
        "order__shop__branch_name",
        ]
    def get_readonly_fields(self, _request, obj=None):
        if (
            obj
        ):  # This is the case when obj is already created i.e. it's an edit
            return [
                "image_tag",
                "order",
                "computed",
                "sha1",
                "extra_data",
                "total",
                "subtotal",
                "tax",
                "item_id",
                "count",
                "item_variation",
                "item_ref",
                "attachements",
                "attachements_tag",
                "indent_extra_data",
            ]
        return []

    filter_horizontal = ["attachements"]
    formfield_overrides = {
        models.CharField: {"widget": TextInput(attrs={"size": "80"})},
        models.JSONField: {
            "widget": Textarea(attrs={"rows": "10", "cols": "60"}),
        },
    }

    def get_fields(self, _request, obj=None):
        if (
            obj
        ):  # This is the case when obj is already created i.e. it's an edit
            return [
                "item_ref",
                "name",
                "image_tag",
                "thumbnail",
                "attachements_tag",
                "order",
                "count",
                "total",
                "subtotal",
                "tax",
                "indent_extra_data",
            ]
        return [
            "name",
            "count",
            "thumbnail",
            "attachements",
            "order",
            "item_id",
            "item_variation",
            "extra_data",
            "total",
            "subtotal",
            "tax",
        ]
