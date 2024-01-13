import logging

from django.conf import settings
from django.core.management.base import (
    BaseCommand,
    no_translations,
)

# pylint: disable=wildcard-import
from .loaders import *


class Command(BaseCommand):
    help = "Loads order data from JSON and ZIP"
    requires_migrations_checks = True

    def add_arguments(self, parser):
        scraper = parser.add_argument_group()
        scraper.add_argument(
            "--init-shops",
            action="store_true",
            help=(
                "Initialize database with shop data from JSON files. Will"
                " update existing data."
            ),
        )

        scraper.add_argument(
            "--import-shop",
            choices=[x.stem for x in settings.INPUT_FOLDER.glob("*.json")]
            + ["all"],
            help="Import order data from shop(s) (default: all)",
        )

        scraper.add_argument(
            "--skip-attachements",
            action="store_true",
            help=(
                "Skip attachements when importing."
            ),
        )

    def setup_logger(self, options):
        log = logging.getLogger(__name__)
        if options["verbosity"] == 0:
            # 0 = minimal output
            log.setLevel(logging.ERROR)
        elif options["verbosity"] == 1:
            # 1 = normal output
            log.setLevel(logging.WARNING)
        elif options["verbosity"] == 2:
            # 2 = verbose output
            log.setLevel(logging.INFO)
        elif options["verbosity"] == 3:
            # 3 = very verbose output
            log.setLevel(logging.DEBUG)
        # pylint: disable=attribute-defined-outside-init
        self.log = log

    @no_translations
    def handle(self, *_, **options):
        options["verbosity"] = 3  # Force debug output

        self.setup_logger(options)
        self.log.debug(options)
        if "import_shop" in options and options["import_shop"]:
            if options["import_shop"] == "all":
                for shop in [
                    x.stem for x in settings.INPUT_FOLDER.glob("*.json")
                ]:
                    ShopOrderLoader(shop, options)
            else:
                ShopOrderLoader(options["import_shop"], options)
        elif "init_shops" in options and options["init_shops"]:
            ShopMetaLoader.load()
        else:
            self.print_help("manage.py", "load")
