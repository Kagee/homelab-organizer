import logging

from django.contrib import admin

from mptt.admin import DraggableMPTTAdmin

from .orderitem import *
from .stockitem import StockItemAdmin
from .order import *
from .shop import *
from .attachement import *
#from .site import HLOAdminSite
from hlo.models import Shop

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
