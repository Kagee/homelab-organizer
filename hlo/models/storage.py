from django.db import models
from django.utils.html import mark_safe

from .commontree import CommonTreeModel


class Storage(CommonTreeModel):
    COLOR_CHOICES = [
        # ruff: noqa: ERA001
        # Optional sub-options
        # (
        #    "No color",
        #    (
        #        ("", "None"),
        #    ),
        # ),
        ("", "None"),
        ("black", "Black"),  # 1f1d1e Eerie Black. Black #000000
        ("blue", "Blue"),  # 0165df True Blue. Blue #0000FF
        ("brown", "Brown"),  # 5d392d Van Dyke Brown. SaddleBrown #8B4513
        ("green", "Green"),  # 017739 Dartmouth Green. SeaGreen #2E8B57
        ("indigo", "Indigo"),  # 2d2684 Cosmic Cobalt. Indigo #4B0082
        ("orange", "Orange"),  # ff7606 Safety Orange. DarkOrange #FF8C00
        ("ping", "Pink"),  # fe538b Strawberry. PaleVioletRed #DB7093
        ("red", "Red"),  # eb243e Imperial Red. Crimson #DC143C
        ("white", "White"),  # e9f4f6 Anti-Flash White. Linen #FAF0E6
        ("yellow", "Yellow"),  # fff003 Yellow Rose. Yellow #FFFF00
    ]
    VALUE_TO_HEX = {
        "black": "#000000",
        "blue": "#0000FF",
        "brown": "#8B4513",
        "green": "#2E8B57",
        "indigo": "#4B0082",
        "orange": "#FF8C00",
        "ping": "#DB7093",
        "red": "#DC143C",
        "white": "#FAF0E6",
        "yellow": "#FFFF00",
    }
    color = models.CharField(
        max_length=20,
        choices=COLOR_CHOICES,
        default="",
        blank=True,
    )

    class Meta:
        verbose_name_plural = "storage"

    def get_hex(self):
        return self.VALUE_TO_HEX[self.color] if self.color else ""

    def get_html_box(self):
        return mark_safe(
            (self.parent.get_html_box() + "&nbsp;" if self.parent else "")
            + '<span style="'
            + "display: inline-block; "
            + "width: 1.2em; "
            + "height: 1.2em; "
            + "border: 3px solid grey; "
            + "margin-top: 0.2em; "
            + "background-color: "
            + self.get_hex()
            + ';"></span>'
            if self.color
            else "",
        )

    def html_rep(self):
        return mark_safe(
            (self.parent.name + "&nbsp;" if self.parent else "")
            + str(self.name)
            + str("&nbsp;&nbsp;&nbsp;" + self.get_html_box()),
        )

    def __str__(self):
        return str(self.name) + str(
            self.VALUE_TO_HEX[self.color] if self.color else "",
        )
