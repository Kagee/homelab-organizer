import logging

from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from django.forms import TextInput, Textarea

from .models import StockItem, Attachement, Order, OrderItem, Shop

logger = logging.getLogger(__name__)

# https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#django.contrib.admin.TabularInline
class OrderStockItemLinkInlineAdmin(admin.TabularInline):
    model = StockItem.orderitems.through
    verbose_name_plural = 'Related order item'
    extra = 1
    fields = ['orderitem',]
    autocomplete_fields = ['orderitem',]

@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    search_fields = ["name", "orderitems__name"]
    def get_inlines(self, request, obj=None):
        # We do this to not kill admin if OrderItem is deleted
        if obj.orderitems.count():
            return [OrderStockItemLinkInlineAdmin,]
        return []
    #fieldsets = [
    #    ("Base properties", {'fields':['name', 'count']}),
    #    (None, {'fields': ('tags',)}),
    #]
    #filter_horizontal = ['tags']


@admin.register(Attachement)
class AttachementAdmin(admin.ModelAdmin):
    search_fields = ["name", "comment", "file"]
    readonly_fields = ["used_by", "text_ornot"]
    def get_fields(self, request, obj=None):
        if (
            obj
        ):  # This is the case when obj is already created i.e. it's an edit
            return [
                "name",
                "comment",
                "type",
                "file",
                "sha1",
                "used_by",
                "text_ornot",
                "text"
            ]
        else:
            return [
                "name",
                "comment",
                "type",
                "file",
                "used_by",
                "text" 
            ]

class AttachementInlineAdmin(admin.TabularInline):
    model = Attachement
    verbose_name_plural = 'Attachements'
    extra = 1
    fields = ['attachements',]
    #autocomplete_fields = ['orderitem',]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    search_fields = ["name", "item_id", "item_variation", "order__shop__branch_name"]
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
                "attachements_tag",
                "indent_extra_data"
            ]
        else:
            return []

    filter_horizontal = ['attachements',]
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
                "indent_extra_data",
            ]
        else:
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


class OrderAdmin(admin.ModelAdmin):

    list_display = ["date", "items_count", "shop_name"]
    list_filter = [
        "shop__name",
    ]
    filter_horizontal = ['attachements',]
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [
                "date",
                "order_url",
                "order_id",
                "items_list",
                "indent_extra_data",
                "attachements",
                "attachements_tag",
                "shop_name",
                "extra_data",
                "indent_extra_data"
            ]
        else:
            return super(OrderAdmin, self).get_readonly_fields(request, obj)

    def get_fields(self, request, obj=None):
        if obj:
            fields = [
                "shop_name",
                "order_id",
                "date",
                "order_url",
                "attachements_tag",   
                "items_list",
                "total",
                "shipping",
                "subtotal",
                "indent_extra_data"
            ]
            if obj.tax:
                fields.append("tax")
            if obj.shipping:
                fields.insert(len(fields)-1, "shipping")
            return fields
        else:
            return super(OrderAdmin, self).get_fields(request, obj)

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
