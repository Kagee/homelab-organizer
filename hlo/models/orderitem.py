import base64
import hashlib
import pprint
from pathlib import Path

from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.utils.html import escape, format_html, mark_safe
from djmoney.models.fields import MoneyField

from . import Attachement, Order


def thumnail_path(instance, filename):
    ext = Path(filename).suffix[1:]
    filename_str = (
        f"{instance.item_id}-"
        f"{ instance.item_variation if instance.item_variation else '' }"
    )
    shopname_b64 = base64.urlsafe_b64encode(
        instance.order.shop.branch_name.encode("utf-8"),
    ).decode("utf-8")
    order_b64 = base64.urlsafe_b64encode(
        instance.order.order_id.encode("utf-8"),
    ).decode("utf-8")
    filename_b64 = base64.urlsafe_b64encode(
        filename_str.encode("utf-8"),
    ).decode("utf-8")
    return f"thumbnails/{shopname_b64}/{order_b64}/{filename_b64}.{ext}"


class OrderItem(models.Model):
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
        blank=True,
        null=True,
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
    attachements = models.ManyToManyField(
        Attachement,
        related_name="orderitem",
    )
    thumbnail = models.ImageField(upload_to=thumnail_path, blank=True)
    # Extra data that we do not import into model
    extra_data = models.JSONField(default=dict, blank=True)

    sha1 = models.CharField(
        max_length=40,
        editable=False,
        default="",
        blank=True,
    )
    # Weak FK for StockItem
    gen_id = models.CharField(max_length=1024, editable=False, unique=True)

    class Meta:
        ordering = ["order__date", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["item_id", "item_variation", "order"],
                name="unique_id_sku_order",
            ),
        ]

    def __str__(self):
        return (
            # pylint: disable=no-member
            f"{self.order.shop.branch_name} item"
            f" #{self.item_id}"
            f"/{self.item_variation}" if len(self.item_variation) else ""
            f": {self.name}"
        )

    def save(self, *args, **kwargs):
        # pylint: disable=no-member
        if self.thumbnail:
            with self.thumbnail.open("rb") as f:
                tbhash = hashlib.sha1()  # noqa: S324
                if f.multiple_chunks():
                    for chunk in f.chunks():
                        tbhash.update(chunk)
                else:
                    tbhash.update(f.read())
                self.sha1 = tbhash.hexdigest()

                super().save(*args, **kwargs)
        else:
            self.sha1 = None
        self.gen_id = (
            f"{self.order.shop.branch_name}-{self.order.order_id}-"
            f"{self.item_id}-"
            f"{self.item_variation}"
            if len(self.item_variation) else "novariation"
        )
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("orderitem", kwargs={"pk": self.pk})

    def image_tag(self, px=150):
        # pylint: disable=no-member
        return mark_safe(
            f'<div style="height: {px}px;"><a href="{self.thumbnail.url}"'
            ' target="_blank"><img style="height: 100%; width: auto;"'
            f' src="{self.thumbnail.url}" width="{self.thumbnail.width}"'
            f' height="{self.thumbnail.height}" /></a></div>',
        )

    image_tag.short_description = "Thumbnail"

    def attachements_tag(self):
        # pylint: disable=no-member
        if self.attachements.count() == 0:
            return "No attachements"
        html = '<ul style="margin: 0;">'
        for attachement in self.attachements.all():
            html += (
                f'<li><a href="{attachement.file.url}"'
                f' target="_blank">{attachement}</a></li>'
            )
        html += "</ul>"
        return mark_safe(html)

    attachements_tag.short_description = "Attachements"

    def item_ref(self):
        return (
            f"{self.item_id}"
            f"{' / ' if len(self.item_variation) else ''}"
            f"{self.item_variation}"
        )

    item_ref.short_description = "Item ID / SKU"

    def get_orderitem_url(self):
        return self.order.shop.item_url_template.format(item_id=self.item_id)

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
