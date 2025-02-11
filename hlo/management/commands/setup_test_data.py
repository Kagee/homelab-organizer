# setup_test_data.py
import random
import sys

import factory.random
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from hlo.factories import ShopFactory
from hlo.models import Shop

NUM_SHOPS = 10
NUM_ORDERS = 100
NUM_ORDER_ITEMS = 1000

# https://mattsegal.dev/django-factoryboy-dummy-data.html


class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        if settings.PROD:
            print("DO NOT RUN IN PROD")  # noqa: T201
            sys.exit(1)

        # factory.random.reseed_random("hlo")

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

        # Add some users to clubs
        # for _ in range(NUM_CLUBS):
        #    club = ClubFactory()
        #    members = random.choices(people, k=USERS_PER_CLUB)
        #    club.user.add(*members)

        # Create all the threads
        # for _ in range(NUM_THREADS):
        #    creator = random.choice(people)
        #    thread = ThreadFactory(creator=creator)
        #    # Create comments for each thread
        #    for _ in range(COMMENTS_PER_THREAD):
        #        commentor = random.choice(people)
        #        CommentFactory(user=commentor, thread=thread)
