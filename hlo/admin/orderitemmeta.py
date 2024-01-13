import logging

from django.contrib import admin

from hlo.models import OrderItemMeta

logger = logging.getLogger(__name__)


@admin.register(OrderItemMeta)
class OrderItemMetaAdmin(admin.ModelAdmin):
    autocomplete_fields = ["parent"]
