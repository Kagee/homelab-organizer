from django.db import models


class StockItem(models.Model):
    #class Meta:
    #    ordering = ["name"]
    #    constraints = [
    #        models.UniqueConstraint(
    #            fields=["item_id", "item_variation", "order"],
    #            name="unique_id_sku_order",
    #        )
    #    ]
    count = models.PositiveIntegerField("number of items", default=1)
    #attachements = GenericRelation(AttachementLink)
    #thumbnail = models.ImageField(upload_to=thumnail_path, blank=True)
