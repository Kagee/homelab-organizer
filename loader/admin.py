from django.contrib import admin
from django.db import models

from django.utils.html import format_html
from django.forms import TextInput, Textarea
from .models import Attachement, AttachementLink, Order, OrderItem, Shop

from rangefilter.filters import DateRangeQuickSelectListFilterBuilder

admin.site.register(Attachement)
admin.site.register(AttachementLink)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
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

    # fields = ('item_ref', 'name', 'count', 'image_tag', 'thumbnail', 'order', 'total', 'extra_data')


# admin.site.register(OrderItem, OrderItemAdmin)


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = [
        lambda obj: obj.shop.list_icon(),
        "date",
        "order_url",
        "items_list",
        "indent_extra_data",
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
