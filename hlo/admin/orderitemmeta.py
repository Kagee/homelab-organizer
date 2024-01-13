import logging

from django.contrib import admin

from ..models import OrderItemMeta

logger = logging.getLogger(__name__)


@admin.register(OrderItemMeta)
class OrderItemMetaAdmin(admin.ModelAdmin):
    autocomplete_fields = ["parent"]
