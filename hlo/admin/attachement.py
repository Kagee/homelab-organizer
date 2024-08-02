from django.contrib import admin

from hlo.models import Attachement


@admin.register(Attachement)
class AttachementAdmin(admin.ModelAdmin):
    search_fields = ["name", "comment", "file"]
    readonly_fields = ["used_by", "text_or_not"]

    def get_fields(self, _request, obj=None):
        if (
            obj
        ):  # This is the case when obj is already created i.e. it's an edit
            return [
                "name",
                "comment",
                "type",
                "file",
                "sha1",
                "used_by",
                "text_or_not",
                "text",
            ]
        return [
            "name",
            "comment",
            "type",
            "file",
            "used_by",
            "text",
        ]


class AttachementInlineAdmin(admin.TabularInline):
    model = Attachement
    verbose_name_plural = "Attachments"
    extra = 1
    fields = ["attachments"]
    # autocomplete_fields = ['orderitem',]  # noqa: ERA001
