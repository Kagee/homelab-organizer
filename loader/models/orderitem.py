import base64
import pprint
from pathlib import Path
import hashlib
from django.contrib import admin
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.html import escape, format_html, mark_safe
from djmoney.models.fields import MoneyField

from .attachementlink import AttachementLink
from .order import Order


def thumnail_path(instance, filename):
    ext = Path(filename).suffix[1:]
    filename_str = (
        f"{instance.order.order_id}-{instance.item_id}-"
        f"{ instance.item_variation if instance.item_variation else '' }"
    )
    shopname_b64 = base64.urlsafe_b64encode(
        instance.order.shop.branch_name.encode("utf-8")
    ).decode("utf-8")
    filename_b64 = base64.urlsafe_b64encode(
        filename_str.encode("utf-8")
    ).decode("utf-8")
    return f"items/thumbnails/{shopname_b64}/{filename_b64}.{ext}"


class OrderItem(models.Model):
    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["item_id", "item_variation", "order"],
                name="unique_id_sku_order",
            )
        ]

    name = models.CharField(max_length=255)
    item_id = models.CharField(
        "Shop item ID",
        max_length=100,
        default="",
        help_text=(
            "The original item id from the shop. Not to be "
            "cofused with the internal database id."
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
    )
    subtotal = MoneyField(
        "Item subtotal",
        max_digits=19,
        decimal_places=4,
        default_currency=None,
        blank=True,
        null=True,
    )
    tax = MoneyField(
        "Item tax/vat",
        max_digits=19,
        decimal_places=4,
        default_currency=None,
        blank=True,
        null=True,
    )
    attachements = GenericRelation(AttachementLink)
    thumbnail = models.ImageField(upload_to=thumnail_path, blank=True)
    # Extra data that we do not import into model
    extra_data = models.JSONField(default=dict, blank=True)

    sha1 = models.CharField(max_length=40, editable=False, default=None, null=True)
    # Weak FK for StockItem
    computed = models.CharField(max_length=1024, editable=False)

    def image_tag(self):
        # pylint: disable=no-member
        return mark_safe(
            f'<a href="{self.thumbnail.url}" target="_blank"><img src="{self.thumbnail.url}" width="150" height="150" /></a>'
        )

    image_tag.short_description = "Thumbnail"

    def item_ref(self):
        return (
            f"{self.item_id}{' / ' if len(self.item_variation) else ''}{self.item_variation}"
        )

    item_ref.short_description = "Item ID / SKU"

    def save(self, *args, **kwargs):
        # pylint: disable=no-member
        if self.thumbnail:
            with self.thumbnail.open("rb") as f:
                hash = hashlib.sha1()
                if f.multiple_chunks():
                    for chunk in f.chunks():
                        hash.update(chunk)
                else:
                    hash.update(f.read())
                self.sha1 = hash.hexdigest()

                super(OrderItem, self).save(*args, **kwargs)
        else:
            self.sha1 = None
        self.computed = (
            f"{self.order.shop.branch_name}-{self.order.order_id}-"
            f"{self.item_id}-{self.item_variation if len(self.item_variation) else 'novariation'}"
        )
        super(OrderItem, self).save(*args, **kwargs)

    @admin.display(description="Order ID")
    def item_url(self):
        return format_html(
            '{} (<a href="{}" target="_blank">Open item page on {}}</a>)',
            self.order_id,
            # pylint: disable=no-member
            self.shop.order_url_template.format(order_id=self.order_id),
            self.shop.branch_name,
        )

    @admin.display(description="Extra data (indented)")
    def indent_extra_data(self):
        return format_html(
            "<pre>{}</pre>",
            escape(pprint.PrettyPrinter(indent=2).pformat(self.extra_data)),
        )

    def __str__(self):
        return (
            # pylint: disable=no-member
            f"{self.order.shop.branch_name} item #{self.item_id}: {self.name}"
        )
