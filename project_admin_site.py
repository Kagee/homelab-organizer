import logging

from django.contrib import admin as a

logger = logging.getLogger(__name__)


class HLOProjectAdminSite(a.AdminSite):
    site_header = "HLO administration"
