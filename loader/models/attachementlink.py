from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from .attachement import Attachement


class AttachementLink(models.Model):
    # The actual attachement object
    attachement = models.ForeignKey(Attachement, on_delete=models.CASCADE)

    # Link to item/order/other that this attachement belongs to
    limit = models.Q(app_label = 'loader', model = 'order') | models.Q(app_label = 'loader', model = 'orderitem')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to = limit)
    object_id = models.PositiveIntegerField()
    attachement_owner = GenericForeignKey()

    def __unicode__(self):
        return (
            f"Attachement '{self.attachement.name}' for {self.object_id} of"
            f" type {self.content_type}"
        )
