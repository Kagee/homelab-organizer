from django.contrib import admin
from django.utils.html import format_html
from mptt.admin import DraggableMPTTAdmin

from hlo.models import Storage


@admin.register(Storage)
class StorageAdmin(DraggableMPTTAdmin):
    list_display = ("tree_actions", "indented_title_color")
    list_display_links = ("indented_title_color",)

    def indented_title_color(self, instance):
        return format_html(
            '<div style="text-indent:{}px">{}</div>',
            # pylint: disable=protected-access
            instance._mpttfield("level") * self.mptt_level_indent,  # noqa: SLF001
            instance.html_rep(),  # Or whatever you want to put here
        )
