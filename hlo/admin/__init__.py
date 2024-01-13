import logging

from .attachement import AttachementAdmin
from .category import CategoryAdmin
from .order import OrderAdmin
from .orderitem import OrderItemAdmin
from .orderitemmeta import OrderItemMetaAdmin
from .project import ProjectAdmin
from .shop import ShopAdmin
from .stockitem import StockItemAdmin
from .storage import StorageAdmin

logger = logging.getLogger(__name__)

__all__ =  [
    "AttachementAdmin",
    "CategoryAdmin",
    "OrderAdmin",
    "OrderItemAdmin",
    "OrderItemMetaAdmin",
    "ProjectAdmin",
    "ShopAdmin",
    "StockItemAdmin",
    "StorageAdmin",
]
