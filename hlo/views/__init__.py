import logging

from .combined_search import item_search
from .commontree import (
    CategoryCreateView,
    CategoryDetailView,
    CategoryListView,
    CategoryUpdateView,
    ProjectCreateView,
    ProjectDetailView,
    ProjectListView,
    ProjectUpdateView,
    StorageCreateView,
    StorageDetailView,
    StorageListView,
    StorageUpdateView,
)
from .index_and_utils import index, no_access, render404
from .label import (
    label_print_orderitem,
    label_print_storage,
    label_render_orderitem,
    label_render_storage,
    sha1_redirect,
)
from .orderitems import (
    OrderItemDetailView,
    OrderItemFilter,
    orderitem_filtered_list,
)
from .orders import OrderDetailView, OrderListView
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
    "no_access",
    "label_render_orderitem",
    "label_print_orderitem",
    "label_render_storage",
    "label_print_storage",
    "sha1_redirect",
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
    "orderitem_filtered_list",
    "OrderDetailView",
    "OrderListView",
]


logger = logging.getLogger(__name__)
