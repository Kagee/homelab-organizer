# setup_test_data.py
import datetime
import random
import sys

import factory.random
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from factory.fuzzy import FuzzyDateTime
from faker import Faker

from hlo.factories import (
    OrderFactory,  # noqa: E402
    ShopFactory,  # noqa: E402
    StorageFactory,  # noqa: E402
)
from hlo.factories.providers import StorageProvider
from hlo.models import Attachment, Order, OrderItem, Shop, StockItem, Storage

factory.Faker.add_provider(StorageProvider)

# Preseed the random generators to a spesific seed
# to make the test data reproducible
random.seed(settings.FACTORY_SEED)
factory.random.reseed_random(settings.FACTORY_SEED)


NUM_SHOPS = 10
NUM_ORDERS = 40
NUM_ORDER_ITEMS = 1000

NUM_BUILDINGS = 5
NUM_ROOMS = 10
NUM_LOCATIONS = 20
NUM_CONTAINERS = 40
# https://mattsegal.dev/django-factoryboy-dummy-data.html


class Command(BaseCommand):
    help = "Generates test data"

    def storage(self):
        buildings = []
        for _ in range(NUM_BUILDINGS):
            building = StorageFactory(
                name=factory.Faker("building"),
                uuid=factory.Faker("uuid4"),
            )
            building.save()
            buildings.append(building)

        rooms = []
        for _ in range(NUM_ROOMS):
            room = StorageFactory(
                name=factory.Faker("room"),
                uuid=factory.Faker("uuid4"),
                parent=random.choice(buildings),  # noqa: S311
            )
            room.save()
            rooms.append(room)

        locations = []
        for _ in range(NUM_LOCATIONS):
            location = StorageFactory(
                name=factory.Faker("location"),
                uuid=factory.Faker("uuid4"),
                parent=random.choice(rooms),  # noqa: S311
            )
            location.save()
            locations.append(location)

        containers = []
        for _ in range(NUM_CONTAINERS):
            container = StorageFactory(
                name=factory.Faker("multiple_items", minimun=2, maximum=10),
                name_secondary=factory.Faker("container"),
                uuid=factory.Faker("uuid4"),
                parent=random.choice(locations),  # noqa: S311
            )
            container.save()
            containers.append(container)

    def orders(self, shops):
        shop_index = list(range(len(shops)))
        weights = [x + 1 * 2 for x in range(len(shops))]
        random.shuffle(weights)
        shop_index_list = random.choices(  # noqa: S311
            shop_index,
            weights=weights,
            k=NUM_ORDERS,
        )

        orders = []
        for _i, shop_index in enumerate(shop_index_list):
            order = OrderFactory.create(shop=shops[shop_index])
            order.save()
            orders.append(order)
        return orders

    @transaction.atomic
    def handle(self, *_args, **_kwargs):
        if settings.PROD:
            print("DO NOT RUN IN PROD")  # noqa: T201
            sys.exit(1)

        self.stdout.write("Deleting old data...")
        models = [Shop, Order, Storage, OrderItem, StockItem, Attachment]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Creating new data...")
        # Create all the users
        shops = []
        for _ in range(NUM_SHOPS):
            shop = ShopFactory()
            shop.save()
            shops.append(shop)

        self.storage()
        orders = self.orders(shops)
        # Faker.date_between_dates(
        #    date_start=
        #    date_end=
        # )
        # orders = []
        # for _i, shop_index in enumerate(shop_index_list):
        #    order = OrderFactory.create(shop=shops[shop_index])
        #    orders.append(order)

        # Create all the threads
        # for _ in range(NUM_THREADS):
        #    creator = random.choice(people)
        #    thread = ThreadFactory(creator=creator)
        #    # Create comments for each thread
        #    for _ in range(COMMENTS_PER_THREAD):
        #        commentor = random.choice(people)
        #        CommentFactory(user=commentor, thread=thread)
