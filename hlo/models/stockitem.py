from django.core.cache import cache
from django.db import models
from django.db.models import Count
from django.urls import reverse
from mptt.fields import TreeManyToManyField  # type: ignore[import-untyped]
from taggit.managers import TaggableManager  # type: ignore[import-untyped]

from . import Attachement


class StockItem(models.Model):
    name = models.CharField(max_length=255, blank=True, default="")
    count = models.PositiveIntegerField("Count", default=0)
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

    def save(self, *args, **kwargs) -> None:
        cache.set(
            "stockitem_count",
            StockItem.objects.count(),
            timeout=None,
        )
        super().save(*args, **kwargs)

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
