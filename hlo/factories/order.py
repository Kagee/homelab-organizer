import datetime
import logging

import factory
from django.conf import settings
from factory import fuzzy
from factory.django import DjangoModelFactory

from hlo.factories import AttachmentFactory
from hlo.factories.providers import MoneyProvider
from hlo.models import Order

logger = logging.getLogger(__name__)

factory.Faker.add_provider(MoneyProvider)


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order
        exclude = ["_currency"]

    _currency = fuzzy.FuzzyChoice(
        settings.CURRENCIES,
    )

    date = factory.Faker(
        "date_between_dates",
        date_start=datetime.datetime(2011, 1, 1, tzinfo=datetime.timezone.utc),
        date_end=datetime.datetime(2024, 12, 24, tzinfo=datetime.timezone.utc),
    )

    # "The original order id from the shop. Not to be "
    # "confused with the internal database id."
    order_id = factory.Faker("uuid4")

    # Money returned: ¥2,748
    subtotal = factory.Faker(
        "djmoney",  # hlo.factories.providers.MoneyProvider
        currency=factory.SelfAttribute(".._currency"),
    )

    # Let's assume a shipping price of 10% of the subtotal
    shipping = factory.Faker(
        "djmoney",  # hlo.factories.providers.MoneyProvider
        currency=factory.SelfAttribute(".._currency"),
        multiplier=0.10,
    )

    # Norwegian tax is calculated as 25% of the subtotal+shipping
    tax = factory.Faker(
        "djmoney",  # hlo.factories.providers.MoneyProvider
        money=factory.List(
            [
                factory.SelfAttribute("..factory_parent.subtotal"),
                factory.SelfAttribute("..factory_parent.shipping"),
            ],
        ),
        multiplier=0.25,
    )

    total = factory.Faker(
        "djmoney",  # hlo.factories.providers.MoneyProvider
        money=factory.List(
            [
                factory.SelfAttribute("..factory_parent.subtotal"),
                factory.SelfAttribute("..factory_parent.shipping"),
                factory.SelfAttribute("..factory_parent.tax"),
            ],
        ),
    )

    """
    attachments = models.ManyToManyField(
        Attachment,
        related_name="order",
        blank=True,
    )
    """
    extra_data = "{}"

    manual_input = False

    @factory.post_generation
    def add_attachments(self, create, extracted, **kwargs):
        logger.debug("Creating attachments for order %s", self.id)
        logger.debug(
            "Create: %s, extracted: %s, kwargs: %s",
            create,
            extracted,
            kwargs,
        )

        # if not create or not extracted:
        if not create:
            return
        # self.save()
        attachment = AttachmentFactory(
            order_id=self.order_id,
            total=self.total,
        )

        logger.debug("Attachment created: %s", attachment)
        # attachment.save()
        self.attachments.add(attachment)
