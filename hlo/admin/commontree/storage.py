from django.contrib import admin
from django.forms.widgets import TextInput
from django.utils.html import format_html
from mptt.admin import DraggableMPTTAdmin  # type: ignore[import-untyped]

from hlo.models import Storage


@admin.register(Storage)
class StorageAdmin(
    DraggableMPTTAdmin,
):
    list_display = ("tree_actions", "indented_title_color")
    list_display_links = ("indented_title_color",)

    def get_readonly_fields(self, request, obj=None):
        return ["sha1_id", *super().get_readonly_fields(request, obj)]

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
