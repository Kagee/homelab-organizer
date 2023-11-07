import hashlib
import base64
from pathlib import Path
import logging

from django.db import models
from django.urls import reverse
from django.utils.html import escape, format_html, format_html_join, mark_safe

logger = logging.getLogger(__name__)


def attachement_file_path(instance, filename):
    assert (
        instance.order.count() < 2
    ), f"Attachement {instance.id} has more than one order"
    assert (
        instance.orderitem.count() < 2
    ), f"Attachement {instance.id} has more than one orderitem"
    if instance.order.count():
        order = instance.order.first()
        shopname_b64 = base64.urlsafe_b64encode(
            order.shop.branch_name.encode("utf-8")
        ).decode("utf-8")
        order_b64 = base64.urlsafe_b64encode(
            order.order_id.encode("utf-8")
        ).decode("utf-8")
        return f"loader/attachements/{shopname_b64}/{order_b64}/{filename}"
    elif instance.orderitem.count():
        orderitem = instance.orderitem.first()
        shopname_b64 = base64.urlsafe_b64encode(
            orderitem.order.shop.branch_name.encode("utf-8")
        ).decode("utf-8")
        order_b64 = base64.urlsafe_b64encode(
            orderitem.order.order_id.encode("utf-8")
        ).decode("utf-8")
        order_item_b64 = base64.urlsafe_b64encode(
            f"{orderitem.item_id}{'-' if len(orderitem.item_variation) else ''}{orderitem.item_variation}"
            .encode("utf-8")
        ).decode("utf-8")
        return f"loader/attachements/{shopname_b64}/{order_b64}/{order_item_b64}/{filename}"
    else:
        raise ValueError(
            "loader.Attachement used on something not order or orderitem"
        )


class Attachement(models.Model):
    DEFAULT_ATTACHEMENT_TYPE = "other"
    ATTACHEMENT_TYPE_CHOICES = [
        ("datasheet", "Datasheet"),
        ("scrape", "Scraped page"),
        ("thumnail", "Thumbnail"),
        ("other", "Other"),
    ]
    name = models.CharField(max_length=255, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, default='')
    type = models.CharField(
        max_length=50,
        choices=ATTACHEMENT_TYPE_CHOICES,
        default=DEFAULT_ATTACHEMENT_TYPE,
    )
    text = models.TextField(blank="", default="")

    # https://docs.djangoproject.com/en/3.2/ref/models/fields/#filefield
    file = models.FileField(
        upload_to=attachement_file_path, max_length=255, blank=True
    )

    sha1 = models.CharField(max_length=40, editable=True)

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
        else:
            return self.orderitem.first()

    def used_by(self):
        # pylint: disable=no-member
        if self.order.count():
            order = self.order.first()
            return format_html(
                '<a href="{}">{} ({})</a>',
                reverse(
                    "admin:loader_order_change",
                    args=(order.id,),
                ),
                order.order_id,
                order.shop.branch_name,
            )
        else:
            orderitem = self.orderitem.first()
            return format_html(
                '<a href="{}">{}</a>',
                reverse(
                    "admin:loader_orderitem_change",
                    args=(orderitem.id,),
                ),
                orderitem.name,
            )

    def save(self, *args, **kwargs):
        # pylint: disable=no-member
        if self.file:
            with self.file.open("rb") as f:
                sha1hash = hashlib.sha1()
                if f.multiple_chunks():
                    for chunk in f.chunks():
                        sha1hash.update(chunk)
                else:
                    sha1hash.update(f.read())
                self.sha1 = sha1hash.hexdigest()
                super(Attachement, self).save(*args, **kwargs)
        else:
            self.sha1 = self.sha1 if self.sha1 else None
        super(Attachement, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.type}) ({Path(self.file.name).name})"
