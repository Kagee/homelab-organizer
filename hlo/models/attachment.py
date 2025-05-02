import hashlib
import logging
from io import BytesIO
from pathlib import Path

from django.contrib import admin
from django.core.cache import cache
from django.core.files import File
from django.db import models
from django.urls import reverse
from django.utils.html import format_html

from hlo.utils.overwritingfilestorage import OverwritingFileSystemStorage

logger = logging.getLogger(__name__)


def attachment_file_path(instance, filename):
    if len(instance.sha1) != 40:  # noqa: PLR2004
        msg = f"SHA1 sum is not 40 chars: {instance.sha1}"
        raise ValueError(msg)
    suffix = Path(filename).suffix
    prefix = instance.sha1[:2]
    filename = instance.sha1[2:]
    return f"attachments/hashed/{prefix}/{filename}{suffix}"


class Attachment(models.Model):
    DEFAULT_ATTACHMENT_TYPE = "other"
    ATTACHMENT_TYPE_CHOICES = [
        ("datasheet", "Datasheet"),
        ("scrape", "Scraped page"),
        ("thumbnail", "Thumbnail"),
        ("other", "Other"),
    ]
    name = models.CharField(max_length=255, blank=True, default="")
    comment = models.CharField(max_length=255, blank=True, default="")
    type = models.CharField(
        max_length=50,
        choices=ATTACHMENT_TYPE_CHOICES,
        default=DEFAULT_ATTACHMENT_TYPE,
    )
    text = models.TextField(blank="", default="")

    # https://docs.djangoproject.com/en/3.2/ref/models/fields/#filefield
    file = models.FileField(
        upload_to=attachment_file_path,
        storage=OverwritingFileSystemStorage(),
        max_length=255,
        blank=True,
    )

    sha1 = models.CharField(max_length=40, editable=True)

    manual_input = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.type}) ({Path(self.file.name).name})"

    def save(self, *args, **kwargs):
        # pylint: disable=no-member
        if self.file:
            #  if self.file and not self.sha1:
            # Maybe do something like checking and
            # saving modification date and recalculate sha1
            # if it is changed
            # buf = BytesIO()
            with self.file.open("rb") as f:
                sha1hash = hashlib.sha1()  # noqa: S324
                if f.multiple_chunks():
                    for chunk in f.chunks():
                        sha1hash.update(chunk)
                        # buf.write(chunk)
                else:
                    data = f.read()
                    sha1hash.update(data)
                    # buf.write(data)
                self.sha1 = sha1hash.hexdigest()
                # buffer_file = File(buf)
                # self.file.file = buffer_file
                logger.debug("Attachment SHA1 set to %s", self.sha1)
                # We must save here because "with self.file above"
                return super().save(*args, **kwargs)
        self.sha1 = self.sha1 if self.sha1 else None
        return super().save(*args, **kwargs)

    def clear_attachment_caches(self):
        """Update cache keys that depend on StockItems."""
        cache.delete_many(
            [
                "attachment_count",
                "attachment_pdf",
                "attachment_html",
            ],
        )

    def text_or_not(self):
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

    @admin.display(description="Manual input")
    def text_manual_input(self) -> str:
        return "Yes" if self.manual_input else "No"

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
