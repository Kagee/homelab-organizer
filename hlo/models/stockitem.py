from django.db import models
from django.db.models import UniqueConstraint
from django.urls import reverse
from mptt.fields import TreeManyToManyField  # type: ignore[import-untyped]
from taggit.managers import TaggableManager  # type: ignore[import-untyped]

from . import Attachement


class StockItem(models.Model):
    name = models.CharField(max_length=255, blank=True, default="")
    count = models.PositiveIntegerField("number of items used", default=0)
    tags = TaggableManager(blank=True)
    category = TreeManyToManyField(
        "Category",
        blank=True,
        related_name="stockitems",
    )
    project = TreeManyToManyField(
        "Project",
        blank=True,
        related_name="stockitems",
    )
    storage = TreeManyToManyField(
        "Storage",
        blank=True,
        related_name="stockitems",
    )
    orderitems = models.ManyToManyField(  # type: ignore[var-annotated]
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

    def __str__(self):
        if self.name:
            return str(self.name)
        return str(self.orderitems.all().first().name)

    def get_absolute_url(self) -> str:
        return reverse("stockitem-detail", kwargs={"pk": self.pk})

    def orderitems_names(self):
        names = []
        if self.orderitems:
            names = [orderitem.name for orderitem in self.orderitems.all()]
        return names

    def thumbnail(self):
        if self.orderitems:
            for orderitem in self.orderitems.all():
                if orderitem.thumbnail:
                    return orderitem.thumbnail.url
        return None


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
            str(
                f"\nOrderitem: {self.orderitem.name}\n"
                f"Stockitem: {self.stockitem.name}",
            )
        )
