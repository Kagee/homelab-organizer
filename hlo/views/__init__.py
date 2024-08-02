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
    label_print_item_size,
    label_print_orderitem,
    label_print_storage,
    label_render_item_size,
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
from .tags import TagDetailView, TagListView, items_with_tags


def test(request):
    import magic

    content_type = "unkown"
    if request.FILES and "uploadFile" in request.FILES:
        content_type = magic.from_buffer(
            request.FILES["uploadFile"].read(), mime=True
        )

    context = {
        "postdata": request.POST,
        "filedata": request.FILES,
        "content_type": content_type,
    }
    return render(request=request, template_name="test.html", context=context)


__all__ = [
    "test",
    "render404",
    "index",
    "no_access",
    "label_render_orderitem",
    "label_print_orderitem",
    "label_render_storage",
    "label_print_storage",
    "label_print_item_size",
    "label_render_item_size",
    "sha1_redirect",
    "AttachmentSearchView",
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
    "OrderUpdateView",
    "OrderCreateView",
    "OrderSimpleCreateView",
    "ShopDetailView",
    "ShopListView",
    "ShopCreateView",
    "ShopUpdateView",
    "TagDetailView",
    "TagListView",
    "items_with_tags",
]


logger = logging.getLogger(__name__)
