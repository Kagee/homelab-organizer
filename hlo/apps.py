from django import apps as dapps

class InventoryConfig(dapps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "hlo"
    verbose_name = "Homelab Inventory"
