from django.db import models

from . import OrderItem


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

    def __str__(self) -> str:
        if self.parent:
            return str(self.parent.name)
        return "Parent is currently not in avaliable in database."
