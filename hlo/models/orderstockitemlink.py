from django.db import models
from django.db.models import UniqueConstraint


class OrderStockItemLink(models.Model):
    orderitem = models.ForeignKey(
        "OrderItem",
        to_field="sha1_id",
        # When OrderItem is deleted, do nothing
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        related_name="stockitem",
    )

    stockitem = models.ForeignKey(
        "StockItem",
        # When StockItem is deleted, delete link
        on_delete=models.CASCADE,
        related_name="orderitem",
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["orderitem", "stockitem"],
                name="unique_orderitem_stockitem",
            ),
        ]

    def __str__(self):
        return (
            # pylint: disable=no-member
            str(
                f"\nOrderitem: {self.orderitem.name}\n"
                f"Stockitem: {self.stockitem.name}",
            )
        )
