import import_export  # type: ignore[import-untyped]
from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin  # type: ignore[import-untyped]

from hlo.models import Project


class ProjectResource(import_export.resources.ModelResource):
    class Meta:
        model = Project
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ("uuid",)
        fields = ("name", "uuid", "parent")

    # We base parent on UUID, as name may be duplicated
    parent = import_export.fields.Field(
        column_name="parent",
        attribute="parent",
        widget=import_export.widgets.ForeignKeyWidget(Project, "uuid"),
    )


@admin.register(Project)
class ProjectAdmin(
    import_export.admin.ImportExportModelAdmin,
    DraggableMPTTAdmin,
):
    list_display = ("tree_actions", "indented_title")
    list_display_links = ("indented_title",)
    resource_class = ProjectResource
