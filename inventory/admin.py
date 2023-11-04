from django.contrib import admin
from .models import StockItem, InventoryTag

class OrderStockItemLinkInlineAdmin(admin.TabularInline):
    model = StockItem.orderitems.through
    verbose_name_plural = 'Related order item'
    extra = 1

class TagsInlineAdmin(admin.TabularInline):
    model = StockItem.tags.through
    verbose_name_plural = 'Tags'
    extra = 1

@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Base properties", {'fields':['name', 'count']}),
        (None, {'fields': ('tags',)}),
    ]
    inlines = (OrderStockItemLinkInlineAdmin,)

@admin.register(InventoryTag)
class InventoryTagAdmin(admin.ModelAdmin):
    list_display = ["name", "color", "name_color_tag"]
