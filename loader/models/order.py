import pprint
from datetime import datetime

from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.utils.html import escape, format_html, format_html_join
from djmoney.models.fields import MoneyField

from .attachement import Attachement
from .shop import Shop


class Order(models.Model):
    class Meta:
        ordering = ["date"]
        constraints = [
            models.UniqueConstraint(
                fields=["shop", "order_id"],
                name="unique_shop_order_id",
            )
        ]

    shop: Shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name="orders",
        editable=False,
    )

    order_id = models.CharField(
        "the original shop order id",
        max_length=100,
        default="",
        help_text=(
            "The original order id from the shop. Not to be "
            "confused with the internal database id."
        ),
        blank=False,
        editable=False,
    )

    date: datetime = models.DateField(
        "Order date",
        editable=True,
    )
    attachements = models.ManyToManyField(
        Attachement,
        related_name="order",
    )
    total = MoneyField(
        max_digits=19,
        decimal_places=4,
        default_currency=None,
    )
    subtotal = MoneyField(
        max_digits=19,
        decimal_places=4,
        default_currency=None,
        blank=True,
        null=True,
    )
    tax = MoneyField(
        max_digits=19,
        decimal_places=4,
        default_currency=None,
        blank=True,
        null=True,
    )
    shipping = MoneyField(
        max_digits=19,
        decimal_places=4,
        default_currency=None,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        "Created at", auto_now_add=True, editable=True
    )
    # Extra data that we do not import into model
    extra_data = models.JSONField(
        default=dict,
        blank=True,
        editable=False,
    )

    @admin.display(description="Items")
    def items_count(self):
        return self.items.count()

    @admin.display(description="Shop")
    def shop_name(self):
        # pylint: disable=no-member
        return self.shop.list_icon()

    @admin.display(description="Items")
    def items_list(self):
        if not self.items.count():
            return "No items in database"
        else:
            return format_html(
                '<ul style="margin: 0;">{}</ul>',
                format_html_join(
                    "\n",
                    '<li><a href="{}">{}</a>&nbsp;&nbsp;(<a target="_blank"'
                    ' href="{}">View on {}</a>)</li>',
                    [
                        (
                            reverse(
                                "admin:loader_orderitem_change",
                                args=(i[1],),
                            ),
                            i[0],
                            # pylint: disable=no-member
                            self.shop.item_url_template.format(item_id=i[2]),
                            self.shop.branch_name,
                        )
                        for i in self.items.all().values_list(
                            "name", "id", "item_id"
                        )
                    ],
                ),
            )

    @admin.display(description="Order URL (generated)")
    def order_url(self):
        # pylint: disable=no-member
        return format_html(
            '{} (<a href="{}" target="_blank">View on {}</a>)',
            self.order_id,
            self.shop.order_url_template.format(order_id=self.order_id),
            self.shop.branch_name,
        )

    @admin.display(description="Extra data")
    def indent_extra_data(self):
        return format_html(
            "<pre>{}</pre>",
            escape(pprint.PrettyPrinter(indent=2).pformat(self.extra_data)),
        )

    @admin.display(description="Order")
    def admin_list_render(self):
        return format_html(
            (  # pylint: disable=no-member
                f'<img src="{self.shop.icon.url}" width="25" />'
                if self.shop.icon
                else ""
            )
            + f"&nbsp;&nbsp;&nbsp; {self.shop.branch_name} order"
            f" #{self.order_id} with {self.items.count()} items"
        )

    def __str__(self):
        return (  # pylint: disable=no-member
            f"{self.shop.branch_name} order #{self.order_id} with"
            # 2pylint: disable=no-member
            f" {self.items.count()} items"
        )
