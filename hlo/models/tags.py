from django.db import models
from django.utils.html import mark_safe
from taggit.models import TagBase, GenericTaggedItemBase


class ColorTag(TagBase):
    DEFAULT_COLOR = "NONE"
    COLOR_CHOICES = [
        ("NONE", "No color"),
        ("#ffee05", "HERMA_YELLOW"),
        ("#e74a24", "HERMA_RED"),
        ("#88d0e3", "HERMA_BLUE"),
        ("#f39402", "HERMA_LUM_ORANGE"),
        ("#72ba5b", "HERMA_GREEN"),
    ]

    color = models.CharField(
        max_length=50,
        choices=COLOR_CHOICES,
        default=DEFAULT_COLOR,
    )

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def name_color(self):
        pass

    def name_color_tag(self):
        # pylint: disable=no-member
        if self.color == "NONE":
            return str(self.name)
        return mark_safe(
            f'<span style="color: {self.color};">{self.name}</span>'
        )


class ColorTagBase(GenericTaggedItemBase):
    tag = models.ForeignKey(
        "ColorTag",
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )
