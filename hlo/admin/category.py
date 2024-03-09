from django.contrib import admin
from import_export import (  # type: ignore[import-untyped]
    fields,
    resources,
    widgets,
)
from import_export.admin import ImportExportModelAdmin
from mptt.admin import DraggableMPTTAdmin

from hlo.models import Category


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        skip_unchanged = True
        report_skipped = True
        exclude = ("id",)
        import_id_fields = ("name",)
        fields = ("parent", "name", "lft", "rght", "tree_id", "level")

    parent = fields.Field(
        column_name="parent",
        attribute="parent",
        widget=widgets.ForeignKeyWidget(Category, "name"),
    )


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin, DraggableMPTTAdmin):
    list_display = ("tree_actions", "indented_title")
    list_display_links = ("indented_title",)
    resource_class = CategoryResource
