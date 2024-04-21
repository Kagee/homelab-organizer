import base64
import hashlib
import logging
from pathlib import Path

from django.db import models
from django.urls import reverse
from django.utils.html import format_html

logger = logging.getLogger(__name__)


def attachement_file_path(instance, filename):
    if instance.order.count() > 1:
        msg = f"Attachement {instance.id} has more than one order"
        raise ValueError(msg)
    if instance.orderitem.count() > 1:
        msg = (
            f"Attachement {instance.id} has more than "
            f"one orderitem: {instance.orderitem.first()}"
        )
        raise ValueError(msg)
    if instance.order.count():
        order = instance.order.first()
        shopname_b64 = base64.urlsafe_b64encode(
            order.shop.branch_name.encode("utf-8"),
        ).decode("utf-8")
        order_b64 = base64.urlsafe_b64encode(
            order.order_id.encode("utf-8"),
        ).decode("utf-8")
        return f"attachements/{shopname_b64}/{order_b64}/{filename}"
    if instance.orderitem.count():
        orderitem = instance.orderitem.first()
        shopname_b64 = base64.urlsafe_b64encode(
            orderitem.order.shop.branch_name.encode("utf-8"),
        ).decode("utf-8")
        order_b64 = base64.urlsafe_b64encode(
            orderitem.order.order_id.encode("utf-8"),
        ).decode("utf-8")
        order_item_b64 = base64.urlsafe_b64encode(
            f"{orderitem.item_id}"
            f"{'-' if len(orderitem.item_variation) else ''}"
            f"{orderitem.item_variation}".encode(),
        ).decode("utf-8")
        return (
            f"attachements/{shopname_b64}/"
            f"{order_b64}/{order_item_b64}/{filename}"
        )
    msg = "Attachement used on something not order or orderitem"
    raise ValueError(
        msg,
    )


class Attachement(models.Model):
    DEFAULT_ATTACHEMENT_TYPE = "other"
    ATTACHEMENT_TYPE_CHOICES = [
        ("datasheet", "Datasheet"),
        ("scrape", "Scraped page"),
        ("thumnail", "Thumbnail"),
        ("other", "Other"),
    ]
    name = models.CharField(max_length=255, blank=True, default="")
    comment = models.CharField(max_length=255, blank=True, default="")
    type = models.CharField(
        max_length=50,
        choices=ATTACHEMENT_TYPE_CHOICES,
        default=DEFAULT_ATTACHEMENT_TYPE,
    )
    text = models.TextField(blank="", default="")

    # https://docs.djangoproject.com/en/3.2/ref/models/fields/#filefield
    file = models.FileField(
        upload_to=attachement_file_path,
        max_length=255,
        blank=True,
    )

    sha1 = models.CharField(max_length=40, editable=True)

    def __str__(self):
        return f"{self.name} ({self.type}) ({Path(self.file.name).name})"

    def save(self, *args, **kwargs):
        # pylint: disable=no-member
        if self.file:
            with self.file.open("rb") as f:
                sha1hash = hashlib.sha1()  # noqa: S324
                if f.multiple_chunks():
                    for chunk in f.chunks():
                        sha1hash.update(chunk)
                else:
                    sha1hash.update(f.read())
                self.sha1 = sha1hash.hexdigest()
                super().save(*args, **kwargs)
        else:
            self.sha1 = self.sha1 if self.sha1 else None
        super().save(*args, **kwargs)

    def text_ornot(self):
        if len(self.text):
            return "There is text"
        return "There is no text"

    def file_name(self):
        if not self.file:
            return ""
        return Path(self.file.name).name

    def get_parent(self):
        # pylint: disable=no-member
        if self.order.count():
            return self.order.first()
        return self.orderitem.first()

    def used_by(self):
        # pylint: disable=no-member
        if self.order.count():
            order = self.order.first()
            return format_html(
                '<a href="{}">{} ({})</a>',
                reverse(
                    "admin:hlo_order_change",
                    args=(order.id,),
                ),
                order.order_id,
                order.shop.branch_name,
            )
        orderitem = self.orderitem.first()
        return format_html(
            '<a href="{}">{}</a>',
            reverse(
                "admin:hlo_orderitem_change",
                args=(orderitem.id,),
            ),
            orderitem.name,
        )
