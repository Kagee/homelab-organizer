import import_export
from django.contrib import admin
from import_export import (  # type: ignore[import-untyped]
    fields,
    resources,
    widgets,
)
from import_export.admin import (  # type: ignore[import-untyped]
    ImportExportModelAdmin,
)

from hlo.models import Category, Project, StockItem, Storage


# https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#django.contrib.admin.TabularInline
class OrderItemStockItemLinkInlineAdmin(admin.TabularInline):
    model = StockItem.orderitems.through
    verbose_name_plural = "Related order item"
    extra = 1
    fields = ["orderitem"]
    autocomplete_fields = ["orderitem"]


class ProjectResource2(import_export.resources.ModelResource):
    # We base parent on UUID, as name may be duplicated
    parent = import_export.fields.Field(
        column_name="parent",
        attribute="parent",
        widget=import_export.widgets.ForeignKeyWidget(Project, "uuid"),
    )


class StockItemResource(import_export.resources.ModelResource):
    class Meta:
        model = StockItem

    category = import_export.fields.Field(
        column_name="category",
        attribute="category",
        widget=import_export.widgets.ManyToManyWidget(
            Category,
            field="uuid",
            # separator=chr(31),
        ),
    )
    storage = import_export.fields.Field(
        column_name="storage",
        attribute="storage",
        widget=import_export.widgets.ManyToManyWidget(
            Storage,
            field="uuid",
            # separator=chr(31),
        ),
    )
    project = import_export.fields.Field(
        column_name="project",
        attribute="project",
        widget=import_export.widgets.ManyToManyWidget(
            Project,
            field="uuid",
            # separator=chr(31),
        ),
    )


@admin.register(StockItem)
class StockItemAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ["name", "orderitems__name"]
    resource_class = StockItemResource

    def get_inlines(self, _request, obj=None):
        # We do this to not kill admin if OrderItem is deleted
        if obj and obj.orderitems.count():
            return [OrderItemStockItemLinkInlineAdmin]
        return []
