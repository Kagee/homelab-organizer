from django.contrib.admin.apps import AdminConfig

# If this is in apps.py, i get
# django.core.exceptions.ImproperlyConfigured:
# Application labels aren't unique, duplicates: admin

class HLOAdminConfig(AdminConfig):
    # Notice that HLOProjectAdminSite and HLOAdminSite are
    # identical, excluding the classname

    # If i do this, only Groups, Users and Taggit models are registered
    #default_site = "hlo.admin.adminsite.HLOAdminSite"  # noqa: ERA001

    # If i do this, all modules above AND all modules registered
    # using admin.register in hlo.admin.* are registered
    default_site = "project_admin_site.HLOProjectAdminSite"
