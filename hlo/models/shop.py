from django.contrib import admin
from django.db import models
from django.utils.html import format_html


class Shop(models.Model):
    name = models.CharField(
        max_length=255,
        help_text=(
            "The name primary shop, Amazon, Distrelec, Adafruit, Kjell.com ..."
        ),
    )
    branch_name = models.CharField(
        max_length=255,
        help_text=(
            "The branch of the primary shop, i.e. Amazon.de"
            " for Amazon, or elfadistrelec.no for Distrelec."
            " default is same as shop name"
        ),
        blank=True,
    )
    icon: models.ImageField = models.ImageField(
        upload_to="shop/icons", blank=True,
    )

    def longname(self):
        # pylint: disable=no-member
        return f"{self.branch_name.capitalize()}" + (
            f", a branch of {self.name}"
            if self.name != self.branch_name
            else ""
        )

    @admin.display(description="Shop")
    def list_icon(self):
        if self.icon:
            return format_html(
                # pylint: disable=no-member
                f'<img src="{self.icon.url}" width="25"'
                f" />&nbsp;{self.longname()}",
            )
        else:
            return f"{self.longname()}"

    list_icon.short_description = "Shop"

    def img_icon(self):
        if self.icon:
            return format_html(
                # pylint: disable=no-member
                f'<img src="{self.icon.url}" style="min-height: 2em; min-width:'
                ' 1em; max-height: 2em;">',
            )
        else:
            return f"{self.longname()[0]}"

    order_url_template = models.CharField(
        max_length=250,
        help_text="The placeholder {order_id} can be used.",
        blank=True,
    )

    item_url_template = models.CharField(
        max_length=250,
        help_text="The placeholders {order_id} and {item_id} can be used.",
        blank=True,
    )

    @admin.display(description="Orders")
    def order_list(self):
        num_orders = self.orders.count()
        if not num_orders:
            return "No orders in database."
        else:
            return num_orders

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "branch_name"],
                name="unique_shop_name_branch_name",
            ),
        ]

    def save(self, *args, **kwargs):
        if not self.branch_name:
            self.branch_name = self.name
        super(Shop, self).save(*args, **kwargs)

    def __str__(self):
        # pylint: disable=no-member
        return f"{self.branch_name.capitalize()}"
