import datetime

import factory
from django.conf import settings
from factory import fuzzy
from factory.django import DjangoModelFactory
from faker_file.providers.pdf_file import PdfFileProvider
from faker_file.storages.filesystem import FileSystemStorage

from hlo.models import Attachment

factory.Faker.add_provider(PdfFileProvider)


class AttachmentFactory(DjangoModelFactory):
    class Meta:
        model = Attachment

    sha1 = factory.Faker("sha1")
