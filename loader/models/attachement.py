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

    def __str__(self):
        return f"{self.name} ({self.type})"
