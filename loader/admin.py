from django.contrib import admin
from django.utils.html import format_html

from .models import Attachement, AttachementLink, Order, OrderItem, Shop

admin.site.register(Attachement)
admin.site.register(AttachementLink)
admin.site.register(OrderItem)


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = [
        lambda obj: obj.shop.list_icon(),
        "date",
        "order_url",
        "items_list",
        "indent_extra_data",
    ]
    list_display = ["admin_list_render"]


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
        "order_list"
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
