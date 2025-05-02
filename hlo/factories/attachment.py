import datetime

import factory
from django.conf import settings
from django.db.models.signals import post_save
from factory import fuzzy
from factory.django import DjangoModelFactory
from faker_file.providers.pdf_file import PdfFileProvider
from faker_file.providers.pdf_file.generators.pdfkit_generator import (
    PdfkitPdfGenerator,
)
from faker_file.storages.filesystem import FileSystemStorage

from hlo.factories.providers import TemplateProvider
from hlo.models import Attachment

factory.Faker.add_provider(PdfFileProvider)
factory.Faker.add_provider(TemplateProvider)


# @factory.django.mute_signals(post_save)
class AttachmentFactory(DjangoModelFactory):
    class Meta:
        model = Attachment
        exclude = ["order_id", "total"]

    sha1 = factory.Faker("sha1")
    manual_input = False
    name = factory.Faker("file_name", category="text", extension="pdf")
    comment = factory.Faker("sentence")

    # We can actually use the text, but this could also be the argument
    # to the pdf generator below, just with more factory_parents.
    text = factory.Faker(
        "template",  # hlo.factories.providers.TemplateProvider
        template="Order {order_id }\nTotal {total}\nName {name}",
        values=factory.Dict(
            {
                "order_id ": factory.SelfAttribute("..factory_parent.order_id"),
                "total": factory.SelfAttribute("..factory_parent.total"),
                "name": factory.Faker("name"),
            }
        ),
    )

    file = factory.django.FileField(
        from_path=factory.Faker(
            "pdf_file",
            content=factory.SelfAttribute("..factory_parent.text"),
            pdf_generator_cls=PdfkitPdfGenerator,
            storage=FileSystemStorage(
                root_path=settings.BASE_DIR,
                rel_path="media_root/faker/",
            ),
        )
    )
