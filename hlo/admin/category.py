import import_export  # type: ignore[import-untyped]
from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin  # type: ignore[import-untyped]

from hlo.models import Category


class CategoryResource(import_export.resources.ModelResource):
    class Meta:
        model = Category
        skip_unchanged = True
        report_skipped = True
        exclude = ("id",)
        import_id_fields = ("uuid",)
        fields = ("parent", "name", "uuid")
        # , "lft", "rght", "tree_id", "level")

    parent = import_export.fields.Field(
        column_name="parent",
        attribute="parent",
        widget=import_export.widgets.ForeignKeyWidget(Category, "uuid"),
    )


@admin.register(Category)
class CategoryAdmin(
    import_export.admin.ImportExportModelAdmin,
    DraggableMPTTAdmin,
):
    list_display = ("tree_actions", "indented_title")
    list_display_links = ("indented_title",)
    resource_class = CategoryResource
