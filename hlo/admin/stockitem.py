import import_export
from django.contrib import admin
from import_export.admin import (  # type: ignore[import-untyped]
    ImportExportModelAdmin,
)

from hlo.models import Category, OrderItem, Project, StockItem, Storage


# https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#django.contrib.admin.TabularInline
class OrderItemStockItemLinkInlineAdmin(admin.TabularInline):
    model = StockItem.orderitems.through
    verbose_name_plural = "Related order item"
    extra = 1
    fields = ["orderitem"]
    autocomplete_fields = ["orderitem"]


class StockItemResource(import_export.resources.ModelResource):
    class Meta:
        model = StockItem
        fields = ("id", "name")  # , "category", "storage", "project"

    # category = import_export.fields.Field(
    #    column_name="category",
    #    attribute="category",
    #    widget=import_export.widgets.ManyToManyWidget(
    #        Category,
    #        field="uuid",
    #    ),
    # )
    # storage = import_export.fields.Field(
    #    column_name="storage",
    #    attribute="storage",
    #    widget=import_export.widgets.ManyToManyWidget(
    #        Storage,
    #        field="uuid",
    #    ),
    # )
    # project = import_export.fields.Field(
    #    column_name="project",
    #    attribute="project",
    #    widget=import_export.widgets.ManyToManyWidget(
    #        Project,
    #        field="uuid",
    #    ),
    # )

    # orderitems = import_export.fields.Field(
    #    column_name="orderitems",
    #    attribute="orderitems",
    #    widget=import_export.widgets.ManyToManyWidget(
    #        OrderItem,
    #        # field="sha1_id",
    #    ),
    # )

    # tags = import_export.fields.Field()
    #    column_name="tags",
    #    attribute="tags",
    #    widget=import_export.widgets.ForeignKeyWidget(Storage, "name"),
    # )

    # def dehydrate_tags(self, item):
    #    return ",".join([tag.name for tag in item.tags.all()])


@admin.register(StockItem)
class StockItemAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ["name", "orderitems__name"]
    resource_class = StockItemResource

    def get_inlines(self, _request, _obj=None):
        # We do this to not kill admin if OrderItem is deleted
        # if obj and obj.orderitems.count():
        return [OrderItemStockItemLinkInlineAdmin]
        # return []
