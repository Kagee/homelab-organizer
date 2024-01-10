import logging

from django.contrib import admin

from mptt.admin import DraggableMPTTAdmin

from .orderitem import OrderItemAdmin
from .stockitem import StockItemAdmin
from .order import OrderAdmin
from .shop import ShopAdmin
from .attachement import AttachementAdmin
from .category import CategoryAdmin
from .project import ProjectAdmin
from .storage import StorageAdmin

logger = logging.getLogger(__name__)
