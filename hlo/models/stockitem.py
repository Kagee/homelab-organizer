from __future__ import annotations

import hashlib
import logging
import uuid
from hashlib import sha1
from io import BytesIO
from pathlib import Path

from django.core.cache import cache
from django.core.files.images import ImageFile
from django.db import models
from django.urls import reverse
from mptt.fields import TreeManyToManyField  # type: ignore[import-untyped]
from taggit.managers import TaggableManager  # type: ignore[import-untyped]

from hlo.utils.overwritingfilestorage import OverwritingFileSystemStorage

from . import Attachement

logger = logging.getLogger(__name__)


def thumnail_path(instance: StockItem, filename: str) -> str:
    if len(instance.thumbnail_sha1) != 40:  # noqa: PLR2004
        msg = f"SHA1 sum is not 40 chars: {instance.thumbnail_sha1}"
        raise ValueError(msg)
    suffix = Path(filename).suffix
    prefix = instance.thumbnail_sha1[:2]
    filename = instance.thumbnail_sha1[2:]
    return f"thumbnails/hashed/{prefix}/{filename}{suffix}"


def make_uuid_sha1():
    return sha1(str(uuid.uuid4()).encode()).hexdigest().upper()  # noqa: S324


class StockItem(models.Model):
    name = models.CharField(max_length=255, blank=True, default="")
    count = models.PositiveIntegerField("Count", default=0)
    count_unit = models.CharField("Unit", default="items", max_length=50)
    comment = models.TextField(blank=True, default="")
    tags = TaggableManager(verbose_name="Tags", help_text=None, blank=True)
    sha1_id = models.CharField(
        max_length=40,
        blank=False,
        null=False,
        default=make_uuid_sha1,
        editable=False,
    )
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

    thumbnail = models.ImageField(
        upload_to=thumnail_path,
        storage=OverwritingFileSystemStorage(),
        blank=True,
    )

    thumbnail_sha1 = models.CharField(
        max_length=40,
        editable=False,
        default="",
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
        # pylint: disable=no-member
        self.thumbnail_sha1 = ""

        buf = BytesIO()
        if self.thumbnail:
            with self.thumbnail.open("rb") as f:
                tbhash = hashlib.sha1()  # noqa: S324
                if f.multiple_chunks():
                    for chunk in f.chunks():
                        tbhash.update(chunk)
                        buf.write(chunk)
                else:
                    data = f.read()
                    tbhash.update(data)
                    buf.write(data)
                self.thumbnail_sha1 = tbhash.hexdigest()
            buffile = ImageFile(buf)
            self.thumbnail.file = buffile
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("stockitem-detail", kwargs={"pk": self.pk})

    def orderitems_names(self):
        names = []
        if self.orderitems:
            names = [orderitem.name for orderitem in self.orderitems.all()]
        return names

    def thumbnail_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        if self.orderitems:
            for orderitem in self.orderitems.all():
                if orderitem.thumbnail:
                    return orderitem.thumbnail.url
        return None
