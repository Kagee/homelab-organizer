import logging

from hlo.views.storage import (
    StorageCreateView,
    StorageDetailView,
    StorageListView,
    StorageUpdateView,
)

from .barcode import barcode_print, barcode_redirect, barcode_render
from .category import (
    CategoryCreateView,
    CategoryDetailView,
    CategoryListView,
    CategoryUpdateView,
)
from .combined_search import item_search
from .index_and_utils import index, render404
from .orderitems import OrderItemDetailView, OrderItemFilter, product_list
from .orders import OrderDetailView, OrderListView
from .project import (
    ProjectCreateView,
    ProjectDetailView,
    ProjectListView,
    ProjectUpdateView,
)
from .search import AttachementSearchView
from .stockitems import (
    StockItemCreate,
    StockItemDetail,
    StockItemFilter,
    StockItemUpdate,
    TagAutoResponseView,
    stockitem_list,
)

__all__ = [
    "render404",
    "index",
    "barcode_redirect",
    "barcode_render",
    "barcode_print",
    "AttachementSearchView",
    "StockItemCreate",
    "StockItemDetail",
    "StockItemFilter",
    "StockItemUpdate",
    "TagAutoResponseView",
    "stockitem_list",
    "ProjectCreateView",
    "ProjectDetailView",
    "ProjectListView",
    "ProjectUpdateView",
    "CategoryCreateView",
    "CategoryDetailView",
    "CategoryListView",
    "CategoryUpdateView",
    "StorageCreateView",
    "StorageDetailView",
    "StorageListView",
    "StorageUpdateView",
    "item_search",
    "OrderItemDetailView",
    "OrderItemFilter",
    "product_list",
    "OrderDetailView",
    "OrderListView",
]


logger = logging.getLogger(__name__)
