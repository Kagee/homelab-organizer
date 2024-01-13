from django.contrib import admin

from ..models import Attachement


@admin.register(Attachement)
class AttachementAdmin(admin.ModelAdmin):
    search_fields = ["name", "comment", "file"]
    readonly_fields = ["used_by", "text_ornot"]
    def get_fields(self, request, obj=None):
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
                "text_ornot",
                "text",
            ]
        else:
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
    verbose_name_plural = "Attachements"
    extra = 1
    fields = ["attachements"]
    #autocomplete_fields = ['orderitem',]
