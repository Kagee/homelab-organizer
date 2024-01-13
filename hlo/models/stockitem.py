from django.db import models
from django.db.models import UniqueConstraint
from django.urls import reverse
from mptt.fields import TreeManyToManyField
from taggit.managers import TaggableManager

from . import Attachement


class StockItem(models.Model):
    name = models.CharField(max_length=255, blank=True)
    count = models.PositiveIntegerField("number of items used", default=0)
    tags = TaggableManager(blank=True)
    category = TreeManyToManyField(
        "Category", blank=True, related_name="stockitems",
    )
    project = TreeManyToManyField(
        "Project",
        blank=True,
        related_name="stockitems",
    )
    storage = TreeManyToManyField(
        "Storage", blank=True, related_name="stockitems",
    )
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


    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                name="unique_name",
            ),
        ]

    def get_absolute_url(self) -> str:
        return reverse("stockitem-detail", kwargs={"pk": self.pk})


    def orderitems_names(self):
        names = []
        if self.orderitems:
            for orderitem in self.orderitems.all():
                names.append(orderitem.name)
        return names

    def thumbnail(self):
        if self.orderitems:
            for orderitem in self.orderitems.all():
                if orderitem.thumbnail:
                    return orderitem.thumbnail.url
        return None

    def __str__(self):
        if self.name:
            return str(self.name)
        return str(self.orderitems.all().first().name)


class OrderStockItemLink(models.Model):
    orderitem = models.ForeignKey(
        "OrderItem",
        to_field="gen_id",
        # When OrderItem is deleted, do nothing
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        related_name="stockitem",
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
            ),
        ]

    def __str__(self):
        return (
            # pylint: disable=no-member
            str(self.orderitem.name)
        )
