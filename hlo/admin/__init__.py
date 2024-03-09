import logging

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
]
