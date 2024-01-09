from django.contrib.admin.apps import AdminConfig


class HLOAdminConfig(AdminConfig):
    default_site = "adminsite.HLOAdminSite"
