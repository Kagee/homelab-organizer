#from django.contrib.admin import apps as aapps
from django.contrib.admin.apps import AdminConfig
#from hlo.admin.site import HLOAdminSite


class HLOAdminConfig(AdminConfig):
    default_site = "hlo.admin.adminsite.HLOAdminSite"
