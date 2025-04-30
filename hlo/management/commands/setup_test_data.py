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

from hlo.models import Shop

# Preseed the random generators to a spesific seed
# to make the test data reproducible
random.seed(settings.FACTORY_SEED)
factory.random.reseed_random(settings.FACTORY_SEED)

from hlo.factories import (
    OrderFactory,  # noqa: E402
    ShopFactory,  # noqa: E402
)

NUM_SHOPS = 10
NUM_ORDERS = 40
NUM_ORDER_ITEMS = 1000

# https://mattsegal.dev/django-factoryboy-dummy-data.html


class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *_args, **_kwargs):
        if settings.PROD:
            print("DO NOT RUN IN PROD")  # noqa: T201
            sys.exit(1)

        self.stdout.write("Deleting old data...")
        models = [Shop]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Creating new data...")
        # Create all the users
        shops = []
        for _ in range(NUM_SHOPS):
            shop = ShopFactory()
            shops.append(shop)

        shop_index = list(range(len(shops)))
        weights = [x + 1 * 2 for x in range(len(shops))]
        random.shuffle(weights)
        # print(shop_index, weights)
        shop_index_list = random.choices(  # noqa: S311
            shop_index,
            weights=weights,
            k=NUM_ORDERS,
        )

        # Faker.date_between_dates(
        #    date_start=
        #    date_end=
        # )
        orders = []
        for _i, shop_index in enumerate(shop_index_list):
            order = OrderFactory.create(shop=shops[shop_index])
            orders.append(order)

        # Create all the threads
        # for _ in range(NUM_THREADS):
        #    creator = random.choice(people)
        #    thread = ThreadFactory(creator=creator)
        #    # Create comments for each thread
        #    for _ in range(COMMENTS_PER_THREAD):
        #        commentor = random.choice(people)
        #        CommentFactory(user=commentor, thread=thread)
