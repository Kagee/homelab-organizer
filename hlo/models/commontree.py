from django.db import models


class CommonTreeModel(models.Model):
    name = models.CharField(
        max_length=50,
        blank=True,  # Should not use null for Char/Text
    )
    text = models.TextField(
        blank=True,  # Should not use null for Char/Text
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="child",
    )

    class Meta:
        abstract = True
