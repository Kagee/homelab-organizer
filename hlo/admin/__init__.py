import logging

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from hlo.models import User

from .attachement import AttachementAdmin
from .category import CategoryAdmin, CategoryResource
from .order import OrderAdmin
from .orderitem import OrderItemAdmin
from .orderitemmeta import OrderItemMetaAdmin
from .project import ProjectAdmin
from .shop import ShopAdmin
from .stockitem import StockItemAdmin, StockItemResource
from .storage import StorageAdmin

logger = logging.getLogger(__name__)

__all__ = [
    "AttachementAdmin",
    "CategoryAdmin",
    "CategoryResource",
    "OrderAdmin",
    "OrderItemAdmin",
    "OrderItemMetaAdmin",
    "ProjectAdmin",
    "ShopAdmin",
    "StockItemAdmin",
    "StockItemResource",
    "StorageAdmin",
    "User",
]

admin.site.register(User, UserAdmin)
