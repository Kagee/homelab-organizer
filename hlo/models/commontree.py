from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class CommonTreeModel(MPTTModel):
    name = models.CharField(
        max_length=50,
        blank=True,  # Should not use null for Char/Text
    )
    text = models.TextField(
        blank=True,  # Should not use null for Char/Text
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )

    class Meta:
        abstract = True