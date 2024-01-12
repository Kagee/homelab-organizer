from django.contrib import admin

from ..models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["date", "items_count", "shop_name"]
    list_filter = [
        "shop__name",
    ]
    filter_horizontal = ['attachements',]
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [
                "date",
                "order_url",
                "order_id",
                "items_list",
                "indent_extra_data",
                "attachements",
                "attachements_tag",
                "shop_name",
                "extra_data",
                "indent_extra_data"
            ]
        return super(OrderAdmin, self).get_readonly_fields(request, obj)

    def get_fields(self, request, obj=None):
        if obj:
            fields = [
                "shop_name",
                "order_id",
                "date",
                "order_url",
                "attachements_tag",   
                "items_list",
                "total",
                "shipping",
                "subtotal",
                "indent_extra_data"
            ]
            if obj.tax:
                fields.append("tax")
            if obj.shipping:
                fields.insert(len(fields)-1, "shipping")
            return fields
        return super().get_fields(request, obj)
