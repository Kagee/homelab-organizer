from django.db import models
from django.db.models import UniqueConstraint


class OrderStockItemLink(models.Model):
    orderitem_link = models.ForeignKey(
        "OrderItem",
        to_field="sha1_id",
        # When OrderItem is deleted, do nothing
        on_delete=models.DO_NOTHING,
        db_constraint=False,
    )

    stockitem_link = models.ForeignKey(
        "StockItem",
        # When StockItem is deleted, delete link
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["orderitem_link", "stockitem_link"],
                name="unique_orderitem_stockitem",
            ),
        ]

    def __str__(self):
        return (
            f"\nOrderitem: {self.orderitem_link.name}\n"
            f"Stockitem: {self.stockitem_link.name}"
        )
