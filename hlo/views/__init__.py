import logging

from django.shortcuts import render

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
    label_print_sha1_size,
    label_render_sha1_size,
    sha1_redirect,
)
from .orderitems import (
    OrderItemCreateView,
    OrderItemDetailView,
    OrderItemUpdateView,
    orderitem_filtered_list,
    orderitem_hide,
)
from .orders import (
    OrderCreateView,
    OrderDetailView,
    OrderListView,
    OrderSimpleCreateView,
    OrderUpdateView,
)
from .search import AttachmentSearchView
from .shop import ShopCreateView, ShopDetailView, ShopListView, ShopUpdateView
from .stockitems import (
    StockItemCreate,
    StockItemDetail,
    # StockItemFilter,
    StockItemUpdate,
    TagAutoResponseView,
    stockitem_list,
)
from .tags import TagDetailView, TagItemListView, TagListView, items_with_tags

__all__ = [
    "AttachmentSearchView",
    "CategoryCreateView",
    "CategoryDetailView",
    "CategoryListView",
    "CategoryUpdateView",
    "OrderCreateView",
    "OrderDetailView",
    "OrderItemCreateView",
    "OrderItemDetailView",
    "OrderItemFilter",
    "OrderItemUpdateView",
    "OrderListView",
    "OrderSimpleCreateView",
    "OrderUpdateView",
    "ProjectCreateView",
    "ProjectDetailView",
    "ProjectListView",
    "ProjectUpdateView",
    "ShopCreateView",
    "ShopDetailView",
    "ShopListView",
    "ShopUpdateView",
    "StockItemCreate",
    "StockItemDetail",
    "StockItemFilter",
    "StockItemUpdate",
    "StorageCreateView",
    "StorageDetailView",
    "StorageListView",
    "StorageUpdateView",
    "TagAutoResponseView",
    "TagDetailView",
    "TagItemListView",
    "TagListView",
    "index",
    "item_search",
    "items_with_tags",
    "label_print_item_size",
    "label_print_orderitem",
    "label_print_sha1_size",
    "label_print_storage",
    "label_render_item_size",
    "label_render_orderitem",
    "label_render_sha1_size",
    "label_render_storage",
    "no_access",
    "orderitem_filtered_list",
    "orderitem_hide",
    "render404",
    "sha1_redirect",
    "stockitem_list",
    "test",
]


logger = logging.getLogger(__name__)
