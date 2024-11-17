from __future__ import annotations

import hashlib
import logging
import pprint
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING

from django.contrib import admin
from django.core.files.images import ImageFile
from django.db import models
from django.urls import reverse
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe
from djmoney.models.fields import MoneyField

from hlo.utils.overwritingfilestorage import OverwritingFileSystemStorage

from . import Attachment, Order

if TYPE_CHECKING:
    from django.utils.safestring import SafeString

logger = logging.getLogger(__name__)


def thumbnail_path(instance: OrderItem, filename: str) -> str:
    if len(instance.thumbnail_sha1) != 40:  # noqa: PLR2004
        msg = f"SHA1 sum is not 40 chars: {instance.thumbnail_sha1}"
        raise ValueError(msg)
    suffix = Path(filename).suffix
    prefix = instance.thumbnail_sha1[:2]
    filename = instance.thumbnail_sha1[2:]
    return f"thumbnails/hashed/{prefix}/{filename}{suffix}"


class OrderItem(models.Model):  # type: ignore[django-manager-missing]
    # the class declaration line in a class that is the target of a ForeignKey
    # from a model with untyped / dynamically added managers as it happens
    # on the reverse relation
    name = models.CharField(max_length=255)
    item_id = models.CharField(
        "Shop item ID",
        max_length=100,
        default="",
        help_text=(
            "The original item id from the shop. Not to be "
            "confused with the internal database id."
        ),
        blank=False,
    )
    item_variation = models.CharField(
        "Item SKU/variation",
        max_length=255,
        default="",
        help_text="The original item sku.",
        blank=True,
    )
    count = models.PositiveIntegerField("number of items", default=1)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    total = MoneyField(
        "Item price",
        max_digits=19,
        decimal_places=4,
        default_currency=None,
        blank=True,
        null=True,
    )  # type: ignore[reportCallIssue]
    subtotal = MoneyField(
        "Item subtotal",
        max_digits=19,
        decimal_places=4,
        default_currency=None,
        blank=True,
        null=True,
    )  # type: ignore[reportCallIssue]
    tax = MoneyField(
        "Item tax/vat",
        max_digits=19,
        decimal_places=4,
        default_currency=None,
        blank=True,
        null=True,
    )  # type: ignore[reportCallIssue]
    attachments = models.ManyToManyField(
        Attachment,
        related_name="orderitem",
        blank=True,
    )

    thumbnail = models.ImageField(
        upload_to=thumbnail_path,  # type: ignore[reportArgumentType]
        storage=OverwritingFileSystemStorage(),
        blank=True,
    )
    # Extra data that we do not import into model
    extra_data = models.JSONField(default=dict, blank=True)

    thumbnail_sha1 = models.CharField(
        max_length=40,
        editable=False,
        default="",
        blank=True,
    )
    # Weak, *static* FK for StockItem
    sha1_id = models.CharField(
        max_length=40,
        unique=True,
    )

    manual_input = models.BooleanField(default=True)

    class Meta:
        ordering = ["order__date", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["item_id", "item_variation", "order"],
                name="unique_id_sku_order",
            ),
        ]

    def __str__(self) -> str:
        """Return string representation.

        Includes shop, order and item id, variation and NameError
        """
        return (
            # pylint: disable=no-member
            f"{self.pk}: {self.order.shop.branch_name} "
            f" #{self.order.order_id}#{self.item_id}"
            f"/{self.item_variation if len(self.item_variation) else ''}"
            f": {self.name}"
        )

    def save(self, *args, **kwargs) -> None:
        self.thumbnail_sha1 = ""

        buf = BytesIO()
        if self.thumbnail:
            with self.thumbnail.open("rb") as f:
                thumbnail_hash = hashlib.sha1()  # noqa: S324
                if f.multiple_chunks():
                    for chunk in f.chunks():
                        thumbnail_hash.update(chunk)
                        buf.write(chunk)
                else:
                    data = f.read()
                    thumbnail_hash.update(data)
                    buf.write(data)
                self.thumbnail_sha1 = thumbnail_hash.hexdigest()
            buffer_file = ImageFile(buf)
            self.thumbnail.file = buffer_file

        item_variation = "novariation"
        if len(self.item_variation):
            item_variation = self.item_variation

        orderitem_hash = hashlib.sha1()  # noqa: S324
        orderitem_hash.update(
            (
                f"{self.order.shop.branch_name}-{self.order.order_id}-"
                f"{self.item_id}-{item_variation}"
            ).encode(),  # defaults to utf-8
        )
        self.sha1_id = orderitem_hash.hexdigest().upper()
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("orderitem-detail", kwargs={"pk": self.pk})

    def simple_image_tag(
        self,
        max_width: int = 300,
        max_height: int = 300,
        classes=None,
        style="",
    ) -> SafeString:
        if classes is None:
            classes = []
        return mark_safe(  # noqa: S308
            f'<img src="{self.thumbnail.url}" class="{" ".join(classes)}" '
            f'style="max-height: {max_height}px; '
            f'max-width: {max_width}px; {style}"/>',
        )

    @admin.display(description="Preview")
    def admin_image_tag(self) -> SafeString:
        return self.simple_image_tag(300, 300)

    def image_tag(self, px: int = 150, max_width: int = 0) -> SafeString:
        # pylint: disable=no-member
        max_width = (
            min(self.thumbnail.width, max_width)
            if max_width
            else self.thumbnail.width
        )
        if px:
            return mark_safe(  # noqa: S308
                f'<div style="height: {px}px;"><a href="{self.thumbnail.url}"'
                ' target="_blank"><img style="height: auto; width: auto;"'
                f' src="{self.thumbnail.url}" width="{self.thumbnail.width}"'
                f' height="{self.thumbnail.height}" /></a></div>',
            )
        return mark_safe(  # noqa: S308
            f'<img style="max-height: 100%; '
            f'width: { f"{max_width} px" if max_width else "auto" };"'
            f' src="{self.thumbnail.url}" />',
        )

    @admin.display(description="Attachments")
    def attachments_tag(self) -> SafeString | str:
        # pylint: disable=no-member
        if self.attachments.count() == 0:
            return "No attachments"
        html = '<ul style="margin: 0;">'
        for attachment in self.attachments.all():
            html += (
                f'<li><a href="{attachment.file.url}"'
                f' target="_blank">{attachment}</a></li>'
            )
        html += "</ul>"
        return mark_safe(html)  # noqa: S308

    @admin.display(description="Item ID / SKU")
    def item_ref(self) -> str:
        return (
            f"{self.item_id}"
            f"{' / ' if len(self.item_variation) else ''}"
            f"{self.item_variation}"
        )

    @admin.display(description="Manual input")
    def text_manual_input(self) -> str:
        return "Yes" if self.manual_input else "No"

    def get_orderitem_url(self) -> str:
        return self.order.shop.item_url_template.format(item_id=self.item_id)

    @admin.display(description="Order ID")
    def item_url(self) -> SafeString:
        return format_html(
            '{} (<a href="{}" target="_blank">Open item page on {}}</a>)',
            self.order_id,  # type: ignore[reportAttributeAccessIssue]
            # pylint: disable=no-member
            self.shop.order_url_template.format(order_id=self.order_id),  # type: ignore[reportAttributeAccessIssue,attr-defined]
            self.shop.branch_name,  # type: ignore[reportAttributeAccessIssue,attr-defined]
        )

    @admin.display(description="Extra data (indented)")
    def indent_extra_data(self) -> SafeString:
        return format_html(
            "<pre>{}</pre>",
            escape(pprint.PrettyPrinter(indent=2).pformat(self.extra_data)),
        )


class OrderItemMeta(models.Model):
    parent = models.OneToOneField(
        OrderItem,
        to_field="sha1_id",
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        related_name="meta",
    )
    hidden = models.BooleanField(default=False)
    label_printed = models.BooleanField(default=False)
    comment = models.CharField(max_length=255, default="", blank=True)
    ai_name = models.CharField(max_length=255, blank=True, default="")

    def __str__(self) -> str:
        """Return name of parent, since meta has no name."""
        if self.parent:
            return str(self.parent.name)
        return "Parent is currently not in available in database."
