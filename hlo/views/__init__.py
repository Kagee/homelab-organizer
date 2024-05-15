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
    OrderItemCreateView,
    OrderItemDetailView,
    OrderItemUpdateView,
    orderitem_filtered_list,
)
from .orders import (
    OrderCreateView,
    OrderDetailView,
    OrderListView,
    OrderUpdateView,
)
from .search import AttachementSearchView
from .shop import ShopCreateView, ShopDetailView, ShopListView, ShopUpdateView
from .stockitems import (
    StockItemCreate,
    StockItemDetail,
    # StockItemFilter,
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
    "OrderItemCreateView",
    "OrderItemUpdateView",
    "orderitem_filtered_list",
    "OrderDetailView",
    "OrderListView",
    "OrderCreateView",
    "OrderUpdateView",
    "ShopDetailView",
    "ShopListView",
    "ShopCreateView",
    "ShopUpdateView",
]


logger = logging.getLogger(__name__)
