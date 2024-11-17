import hashlib
import uuid

from django.db import models
from mptt.models import (  # type: ignore[import-untyped]
    MPTTModel,
    TreeForeignKey,
)


class CommonTreeModel(MPTTModel):
    name: models.CharField = models.CharField(
        max_length=255,
        blank=False,  # Should not use null for Char/Text
    )

    name_secondary: models.CharField = models.CharField(
        max_length=255,
        blank=True,  # Should not use null for Char/Text
    )

    comment: models.TextField = models.TextField(
        blank=True,  # Should not use null for Char/Text
    )

    uuid: models.UUIDField = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
    )

    sha1_id: models.CharField = models.CharField(
        max_length=40,
        editable=False,
        blank=True,
    )

    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )

    label_printed: models.BooleanField = models.BooleanField(default=False)

    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        uuid_sha1 = hashlib.sha1()  # noqa: S324
        uuid_sha1.update(str(self.uuid).encode())  # defaults to utf-8
        self.sha1_id = uuid_sha1.hexdigest().upper()
        super().save(*args, **kwargs)

    class MPTTMeta:
        order_insertion_by = ["name"]
