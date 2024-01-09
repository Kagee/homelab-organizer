import logging

from django.contrib import admin

from mptt.admin import DraggableMPTTAdmin

from .orderitem import OrderItemAdmin
from .stockitem import StockItemAdmin
from .order import OrderAdmin
from .shop import ShopAdmin
from .attachement import AttachementAdmin

from ..models import Category, Project, Storage

logger = logging.getLogger(__name__)


admin.site.register(
    Category,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
        # ...more fields if you feel like it...
    ),
    list_display_links=(
        'indented_title',
    ),
)
admin.site.register(
    Project,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
        # ...more fields if you feel like it...
    ),
    list_display_links=(
        'indented_title',
    ),
)
admin.site.register(
    Storage,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
        # ...more fields if you feel like it...
    ),
    list_display_links=(
        'indented_title',
    ),
)

#@admin.register(Category)
#class CategoryAdmin(admin.ModelAdmin):
#    pass
#
#@admin.register(Project)
#class ProjectAdmin(admin.ModelAdmin):
#    pass
#
#@admin.register(Storage)
#class StorageAdmin(admin.ModelAdmin):
#    pass
