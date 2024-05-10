from django.contrib import admin
from django.db import models
from django.forms import Textarea, TextInput

from hlo.models import OrderItem, OrderItemMeta, OrderStockItemLink


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
            if obj.manual_input:
                return [
                    "admin_image_tag",
                    "order",
                    "text_manual_input",
                    "computed",
                    "sha1",
                    "item_id",
                    "item_variation",
                    "item_ref",
                    "attachements",
                    "attachements_tag",
                    "indent_extra_data",
                ]
            else:
                return [
                    "admin_image_tag",
                    "name",
                    "order",
                    "text_manual_input",
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
                "admin_image_tag",
                "thumbnail",
                "text_manual_input",
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
            "text_manual_input",
            "attachements",
            "order",
            "item_id",
            "item_variation",
            "extra_data",
            "total",
            "subtotal",
            "tax",
        ]


@admin.register(OrderItemMeta)
class OrderItemMetaAdmin(admin.ModelAdmin):
    autocomplete_fields = ["parent"]


@admin.register(OrderStockItemLink)
class OrderStockItemLinkAdmin(admin.ModelAdmin):
    pass
