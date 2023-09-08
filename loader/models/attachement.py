from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Attachement(models.Model):
    ATTACHEMENT_TYPE_CHOICES = [
        ("datasheet", "Datasheet"),
        ("scrape", "Scraped page"),
        ("thumnail", "Thumbnail"),
        ("other", "Other"),
    ]
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=ATTACHEMENT_TYPE_CHOICES)
    url = models.CharField(max_length=255, blank=True)
    # https://docs.djangoproject.com/en/3.2/ref/models/fields/#filefield
    file = models.FileField(upload_to="attachements/", max_length=255)
    # Detected mimetype?
    filetype = models.CharField(max_length=50, blank=True)


    # GenericForeignKey so Attachement can be used by "any" model
    # https://stackoverflow.com/a/51734432
    generic_foreign_key_limit = models.Q(
        app_label="loader", model="order"
    ) | models.Q(app_label="loader", model="orderitem")

    ref_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=generic_foreign_key_limit,
    )

    ref_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("ref_type", "ref_id")


    def __str__(self):
        return f"{self.name} ({self.type})"
