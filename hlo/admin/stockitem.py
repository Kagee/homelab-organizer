from django.contrib import admin
from import_export import (  # type: ignore[import-untyped]
    fields,
    resources,
    widgets,
)
from import_export.admin import ImportExportModelAdmin

from hlo.models import Category, Project, StockItem, Storage


# https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#django.contrib.admin.TabularInline
class OrderItemStockItemLinkInlineAdmin(admin.TabularInline):
    model = StockItem.orderitems.through
    verbose_name_plural = "Related order item"
    extra = 1
    fields = ["orderitem"]
    autocomplete_fields = ["orderitem"]


class StockItemResource(resources.ModelResource):
    class Meta:
        model = StockItem

    category = fields.Field(
        column_name="category",
        attribute="category",
        widget=widgets.ManyToManyWidget(Category, field="name", separator="$"),
    )
    storage = fields.Field(
        column_name="storage",
        attribute="storage",
        widget=widgets.ManyToManyWidget(Storage, field="name", separator="$"),
    )
    project = fields.Field(
        column_name="project",
        attribute="project",
        widget=widgets.ManyToManyWidget(Project, field="name", separator="$"),
    )


@admin.register(StockItem)
class StockItemAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ["name", "orderitems__name"]
    resource_class = StockItemResource

    def get_inlines(self, _request, obj=None):
        # We do this to not kill admin if OrderItem is deleted
        if obj.orderitems.count():
            return [OrderItemStockItemLinkInlineAdmin]
        return []
