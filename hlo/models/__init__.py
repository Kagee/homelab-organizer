import contextlib
import logging

from django.contrib.auth.models import AbstractUser

from .attachment import Attachment
from .commontree import Category, Project, Storage
from .order import Order
from .orderitem import OrderItem, OrderItemMeta
from .orderstockitemlink import OrderStockItemLink
from .shop import Shop
from .stockitem import StockItem

logger = logging.getLogger(__name__)


class User(AbstractUser):
    pass


def get_object_from_sha1(
    sha1: str,
) -> tuple[OrderItem | StockItem | Storage | None, type | None]:
    """Return object and type based on SHA1."""
    sha1 = sha1.upper()
    obj: Storage | StockItem | OrderItem
    with contextlib.suppress(Storage.DoesNotExist):
        obj = Storage.objects.get(sha1_id=sha1)
        return obj, Storage
    with contextlib.suppress(StockItem.DoesNotExist):
        obj = StockItem.objects.get(sha1_id=sha1)
        return obj, StockItem
    with contextlib.suppress(OrderItem.DoesNotExist):
        obj = OrderItem.objects.get(sha1_id=sha1)
        return obj, OrderItem
    logger.debug("SHA1 did not match anything: %s", sha1)
    return None, None


__all__ = [
    "Attachment",
    "Category",
    "Order",
    "OrderItem",
    "OrderItemMeta",
    "OrderStockItemLink",
    "Project",
    "Shop",
    "StockItem",
    "Storage",
    "User",
    "get_object_from_sha1",
]
