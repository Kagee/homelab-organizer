import datetime
import logging

import factory
from django.conf import settings
from factory import fuzzy
from factory.django import DjangoModelFactory

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

    # attachments = AttachmentFactory.generate_batch(
    #    strategy=factory.CREATE_STRATEGY,
    #    size=2,
    # )

    # Money returned: ¥2,748
    subtotal = factory.Faker(
        "djmoney",
        currency=factory.SelfAttribute(".._currency"),
    )

    # Let's assume a shipping price of 10% of the subtotal
    shipping = factory.Faker(
        "djmoney",
        currency=factory.SelfAttribute(".._currency"),
        multiplier=0.10,
    )

    # Norwegian tax is calculated as 25% of the subtotal+shipping
    tax = factory.Faker(
        "djmoney",
        money=factory.List(
            [
                factory.SelfAttribute("..factory_parent.subtotal"),
                factory.SelfAttribute("..factory_parent.shipping"),
            ],
        ),
        multiplier=0.25,
    )

    total = factory.Faker(
        "djmoney",
        money=factory.List(
            [
                factory.SelfAttribute("..factory_parent.subtotal"),
                factory.SelfAttribute("..factory_parent.shipping"),
                factory.SelfAttribute("..factory_parent.tax"),
            ],
        ),
    )

    # total = factory.Faker(
    #    "djmoney",
    #    money=[
    #        factory.LazyAttribute(lambda o: o.subtotal),
    #        factory.LazyAttribute(lambda o: o.tax),
    #    ],
    # )
    # shipping = factory.Faker("djmoney", currency=_currency, multiplier=0.10)
    # tax = factory.Faker("djmoney", money=subtotal, multiplier=0.25)

    # @factory.lazy_attribute
    # def subtotal(self):
    #    return factory.Faker("djmoney", currency=self._currency)
    # return Money(amount="1220.90", currency=self._currency)

    # factory.Faker("money", text="@%#,##")

    # @factory.post_generation
    # def total(self, create, _value, **_kwargs):
    #    if not create:
    #        return
    #    self.tax = ((self.subtotal or 0.0) + (self.shipping or 0.0)) * 0.25
    #    self.total = (
    #        (self.subtotal or 0.0) + (self.tax or 0.0) + (self.shipping or 0.0)
    #    )

    # if value:
    #    # User called MyFactory(my_m2m=an_instance)
    #    for a in value:
    #        self.my_m2ms.add(a)

    # [
    #    factory.Faker(
    #        "pdf_file",
    #        storage=FileSystemStorage(
    #            root_path=settings.MEDIA_ROOT,
    #            rel_path="faker",
    #        ),
    #    )
    # ]

    # @factory.post_generation
    # def groups(self, create, extracted, **kwargs):
    #    if not create or not extracted:
    #        # Simple build, or nothing to add, do nothing.
    #        return#
    #
    #        # Add the iterable of groups using bulk addition
    #        self.groups.add(*extracted)

    """
    attachments = models.ManyToManyField(
        Attachment,
        related_name="order",
        blank=True,
    )
    
    fake.numerify("@%#,##")
    total = MoneyField(
        max_digits=19,
        decimal_places=4,
        default_currency=None,
        blank=True,
        null=True,
    )
    subtotal = MoneyField(
        max_digits=19,
        decimal_places=4,
        default_currency=None,
        blank=True,
        null=True,
    )
    tax = MoneyField(
        max_digits=19,
        decimal_places=4,
        default_currency=None,
        blank=True,
        null=True,
    )
    shipping = MoneyField(
        max_digits=19,
        decimal_places=4,
        default_currency=None,
        blank=True,
        null=True,
    )
    """
    extra_data = "{}"

    manual_input = False

    # @factory.post_generation
    # def shop(self, create, extracted, **_kwargs):
    #    if not create or not extracted:
    #        # Simple build, or nothing to add, do nothing.
    #        return#
    #
    #       # Add the iterable of groups using bulk addition
    #      self.shop.add(extracted["shop"])
