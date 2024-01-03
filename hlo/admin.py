import logging
from django.contrib import admin
from .models import StockItem, ColorTag

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


@admin.register(ColorTag)
class ColorTagAdmin(admin.ModelAdmin):
    list_display = ["name", "color", "name_color_tag"]