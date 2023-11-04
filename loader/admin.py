from django.contrib import admin
from django.db import models

from django.utils.html import format_html
from django.forms import TextInput, Textarea
from rangefilter.filters import DateRangeQuickSelectListFilterBuilder

from .models import Attachement, Order, OrderItem, Shop

admin.site.register(Attachement)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    search_fields = ["name", "item_id", "item_variation"]
    def get_readonly_fields(self, request, obj=None):
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
                "attachements_tag"
            ]
        else:
            return []

    formfield_overrides = {
        models.CharField: {"widget": TextInput(attrs={"size": "80"})},
        models.JSONField: {
            "widget": Textarea(attrs={"rows": "10", "cols": "60"})
        },
    }

    def get_fields(self, request, obj=None):
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
                "extra_data",
                
            ]
        else:
            return [
                "name",
                "count",
                "thumbnail",
                "order",
                "item_id",
                "item_variation",
                "extra_data",
                "total",
                "subtotal",
                "tax",
            ]


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = [
        lambda obj: obj.shop.list_icon(),
        "date",
        "order_url",
        "items_list",
        "indent_extra_data",
        "attachements"
    ]
    list_display = ["date", "items_count", "shop_name"]
    list_filter = [
        "shop__name",
        ("date", DateRangeQuickSelectListFilterBuilder()),
    ]


admin.site.register(Order, OrderAdmin)


class ShopAdmin(admin.ModelAdmin):
    list_display = ["list_icon", "id", "order_list"]
    readonly_fields = ["id", "change_icon", "order_list"]
    fields = [
        "id",
        "name",
        "branch_name",
        "icon",
        "change_icon",
        "order_url_template",
        "item_url_template",
        "order_list",
    ]

    @admin.display(description="Icon preview")
    def change_icon(self, instance):
        return (
            format_html(f'<img src="{instance.icon.url}" width="75" />')
            if instance.icon
            else ""
        )

    # pylint: disable=arguments-differ
    # they do not?
    def get_form(self, request, obj=None, **kwargs):
        form = super(ShopAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["order_url_template"].widget.attrs[
            "style"
        ] = "width: 45em;"
        form.base_fields["item_url_template"].widget.attrs[
            "style"
        ] = "width: 45em;"
        return form


admin.site.register(Shop, ShopAdmin)
