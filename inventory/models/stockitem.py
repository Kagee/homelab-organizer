from django.db import models
from django.db.models import UniqueConstraint
from taggit.managers import TaggableManager
from .taggit import TaggedStock


class OrderStockItemLink(models.Model):
    orderitem = models.ForeignKey(
        "loader.OrderItem",
        to_field="gen_id",
        # When OrderItem is deleted, do nothing
        on_delete=models.DO_NOTHING,
        related_name="orderitem",
        db_constraint=False,
    )
    stockitem = models.ForeignKey(
        "StockItem",
        # When StockItem is deleted, delete link
        on_delete=models.CASCADE,
        related_name="stockitem",
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["orderitem", "stockitem"],
                name="unique_orderitem_stockitem",
            )
        ]

    def __str__(self):
        return (
            # pylint: disable=no-member
            str(self.orderitem.name)
        )


class StockItem(models.Model):
    # class Meta:
    #    ordering = ["name"]
    #    constraints = [
    #        models.UniqueConstraint(
    #            fields=["item_id", "item_variation", "order"],
    #            name="unique_id_sku_order",
    #        )
    #    ]
    name = models.CharField(max_length=255, null=True, blank=True)
    count = models.PositiveIntegerField("number of items used", default=0)
    tags = TaggableManager(through=TaggedStock)
    orderitems = models.ManyToManyField(
        "loader.OrderItem",
        through="OrderStockItemLink",
        related_name="orderitems",
    )
