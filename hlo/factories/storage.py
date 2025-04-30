import datetime

import factory
from django.conf import settings
from factory import fuzzy
from factory.django import DjangoModelFactory
from faker_file.providers.pdf_file import PdfFileProvider
from faker_file.storages.filesystem import FileSystemStorage

from hlo.factories.providers import StorageProvider
from hlo.models import Storage


class StorageFactory(DjangoModelFactory):
    class Meta:
        model = Storage

    """
    name

    name_secondary

    comment

    uuid # autimaitc, but whould probably be made

    sha1_id # calculated

    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    """
