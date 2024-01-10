from django.db import models
from django.utils.html import mark_safe
from . import CommonTreeModel


class Storage(CommonTreeModel):
    COLOR_CHOICES = [
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
        null=True,
    )

    class Meta:
        verbose_name_plural = "storage"

    def html_rep(self):
        return mark_safe(
            str(self.name)
            + str(
                '&nbsp;<span style="color: '
                + self.VALUE_TO_HEX[self.color]
                + '">██</span>'
                if self.color
                else ""
            )
        )

    def __str__(self):
        return str(self.name) + str(
            self.VALUE_TO_HEX[self.color] if self.color else ""
        )
