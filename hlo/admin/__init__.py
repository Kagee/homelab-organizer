import logging

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from hlo.models import User

from .attachment import AttachmentAdmin
from .commontree import CategoryAdmin, ProjectAdmin, StorageAdmin
from .order import OrderAdmin
from .orderitem import (
    OrderItemAdmin,
    OrderItemMetaAdmin,
    OrderStockItemLinkAdmin,
)
from .shop import ShopAdmin
from .stockitem import StockItemAdmin

logger = logging.getLogger(__name__)

__all__ = [
    "AttachmentAdmin",
    "CategoryAdmin",
    "CategoryResource",
    "OrderAdmin",
    "OrderItemAdmin",
    "OrderItemMetaAdmin",
    "OrderStockItemLinkAdmin",
    "ProjectAdmin",
    "ShopAdmin",
    "StockItemAdmin",
    "StorageAdmin",
    "User",
]

admin.site.register(User, UserAdmin)
