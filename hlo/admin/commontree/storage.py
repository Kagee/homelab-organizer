import import_export  # type: ignore[import-untyped]
from django.contrib import admin
from django.forms.widgets import Textarea, TextInput
from django.utils.html import format_html
from mptt.admin import DraggableMPTTAdmin  # type: ignore[import-untyped]

from hlo.models import Storage


class StorageResource(import_export.resources.ModelResource):
    class Meta:
        model = Storage
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ("uuid",)
        fields = ("name", "uuid", "parent")

    # We base parent on UUID, as name may be duplicated
    parent = import_export.fields.Field(
        column_name="parent",
        attribute="parent",
        widget=import_export.widgets.ForeignKeyWidget(Storage, "uuid"),
    )


@admin.register(Storage)
class StorageAdmin(
    import_export.admin.ImportExportModelAdmin,
    DraggableMPTTAdmin,
):
    list_display = ("tree_actions", "indented_title_color")
    list_display_links = ("indented_title_color",)
    resource_class = StorageResource

    def get_form(self, request, obj=None, change=False, **kwargs):  # noqa: FBT002
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields["name"].widget = TextInput(
            attrs={"size": 100},
        )
        form.base_fields["name_secondary"].widget = TextInput(
            attrs={"size": 100},
        )
        return form

    def indented_title_color(self, instance):
        return format_html(
            '<div style="text-indent:{}px">{}</div>',
            # pylint: disable=protected-access
            instance._mpttfield("level") * self.mptt_level_indent,  # noqa: SLF001
            instance.html_rep(),  # Or whatever you want to put here
        )
