from django.db import models
from django.urls import reverse
from django.db.models import UniqueConstraint

from taggit.managers import TaggableManager

from . import Attachement


class StockItem(models.Model):
    def get_absolute_url(self):
        return reverse("stockitem-detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                name="unique_name",
            )
        ]

    name = models.CharField(max_length=255, null=True, blank=True)
    count = models.PositiveIntegerField("number of items used", default=0)
    tags = TaggableManager(blank=True)
    #category
    #project
    #storage
    orderitems = models.ManyToManyField(
        "OrderItem",
        through="OrderStockItemLink",
        related_name="stockitems",
        blank=True,
    )
    attachements = models.ManyToManyField(
        Attachement,
        related_name="attachements",
        blank=True,
    )


class OrderStockItemLink(models.Model):
    orderitem = models.ForeignKey(
        "OrderItem",
        to_field="gen_id",
        # When OrderItem is deleted, do nothing
        on_delete=models.DO_NOTHING,
        related_name="stockitem",
        db_constraint=False,
    )
    stockitem = models.ForeignKey(
        "StockItem",
        # When StockItem is deleted, delete link
        on_delete=models.CASCADE,
        related_name="orderitem",
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
