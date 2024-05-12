from django.contrib import admin

from hlo.models import StockItem


# https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#django.contrib.admin.TabularInline
class OrderItemStockItemLinkInlineAdmin(admin.TabularInline):
    model = StockItem.orderitems.through
    verbose_name_plural = "Related order item"
    extra = 1
    fields = ["orderitem_link"]
    autocomplete_fields = ["orderitem_link"]


@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    search_fields = ["name", "orderitems__name"]

    def get_inlines(self, _request, _obj=None):
        # We do this to not kill admin if OrderItem is deleted
        # if obj and obj.orderitems.count():
        return [OrderItemStockItemLinkInlineAdmin]
        # return []
