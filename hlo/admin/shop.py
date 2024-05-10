from django.contrib import admin
from django.utils.html import format_html

from hlo.models import Shop


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ["list_icon", "id", "order_list", "text_manual_input"]
    fields = [
        "name",
        "branch_name",
        "id",
        "text_manual_input",
        "icon",
        "change_icon",
        "order_url_template",
        "item_url_template",
        "order_list",
    ]

    def get_readonly_fields(self, _request, obj=None):
        if (
            obj
        ):  # This is the case when obj is already created i.e. it's an edit
            if obj.manual_input:
                return [
                    "id",
                    "change_icon",
                    "order_list",
                    "text_manual_input",
                ]
            return [
                "id",
                "change_icon",
                "order_list",
                "text_manual_input",
                "name",
                "branch_name",
            ]
        return []

    @admin.display(description="Icon preview")
    def change_icon(self, instance):
        return (
            format_html(f'<img src="{instance.icon.url}" width="75" />')
            if instance.icon
            else ""
        )

    # pylint: disable=arguments-differ
    # they do not?
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["order_url_template"].widget.attrs["style"] = (
            "width: 45em;"
        )
        form.base_fields["item_url_template"].widget.attrs["style"] = (
            "width: 45em;"
        )
        return form
