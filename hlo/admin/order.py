import json

from django.contrib import admin

from hlo.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "date",
        "items_count",
        "shop_name",
        "text_manual_input",
        "total",
    ]
    list_filter = [
        "shop__name",
    ]
    filter_horizontal = ["attachements"]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if obj.manual_input:
                return [
                    "date",
                    "text_manual_input",
                    "order_url",
                    "order_id",
                    "items_list",
                    "indent_extra_data",
                    "attachements",
                    "attachements_tag",
                    "shop_name",
                    "extra_data",
                    "indent_extra_data",
                ]
            return [
                "date",
                "text_manual_input",
                "order_url",
                "order_id",
                "items_list",
                "indent_extra_data",
                "attachements",
                "attachements_tag",
                "shop_name",
                "extra_data",
                "indent_extra_data",
                "total",
                "shipping",
                "subtotal",
                "tax",
            ]
        return super().get_readonly_fields(request, obj)

    def get_fields(self, request, obj=None):
        if obj:
            fields = [
                "shop_name",
                "order_id",
                "text_manual_input",
                "date",
                "order_url",
            ]

            if obj.manual_input or obj.attachements.all():
                fields += ["attachements_tag"]

            fields += ["items_list"]

            if obj.manual_input or obj.shipping:
                fields += ["shipping"]
            if obj.manual_input or obj.subtotal:
                fields += ["subtotal"]
            if obj.manual_input or obj.tax:
                fields += ["tax"]
            if obj.manual_input or obj.total:
                fields += ["total"]
            if obj.manual_input or obj.extra_data:
                fields += ["indent_extra_data"]

            return fields
        return super().get_fields(request, obj)
