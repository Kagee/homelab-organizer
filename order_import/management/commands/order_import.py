import logging
import os
#from datetime import datetime
from django.conf import settings
from django.core.files import File
from django.core.management.base import (BaseCommand,# CommandError,
                                         no_translations)
#from djmoney.money import Money
#from price_parser import Price

#from ...models import Order, OrderItem, Shop  # , Attachement
from ...models import Shop


class Command(BaseCommand):
    help = "Scrapes a webshop for orders using Selenium"
    requires_migrations_checks = True

    def add_arguments(self, parser):
        scraper = parser.add_argument_group()
        # Apparently we do not support subparsers
        scraper.add_argument(
            "--init-shops",
            action="store_true",
            help=(
                "Initialize database with some data. "
                "Can be used to update data."
            ),
        )
        scraper.add_argument(
            "--load-to-db",
            action="store_true",
            help="Load all currently parsed data to DB.",
        )
        scraper.add_argument(
            "--db-to-csv",
            action="store_true",
            help="Put db fields in CSV",
        )
        scraper.add_argument(
            "--db-shop-id",
            type=int,
            default=-1,
            choices=list(Shop.objects.values_list("id", flat=True)),
            help="Load data into this database shop. "
            + ", ".join(
                f"{x[0]} - {x[1]}"
                for x in Shop.objects.values_list("id", "branch_name")
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
        if options["init_shops"]:
            self.setup_logger(options)
            self.log.debug("Initializing database with shops")
            for shop in [
                (
                    "Adafruit",
                    None,
                    (
                        "https://www.adafruit.com/index.php?"
                        "main_page=account_history_info&order_id={order_id}"
                    ),
                    "https://www.adafruit.com/product/{item_id}",
                ),
                (
                    "Amazon",
                    "Amazon.de",
                    "https://www.amazon.de/gp/your-account/order-details/?orderID={order_id}",
                    "https://www.amazon.de/-/en/gp/product/{item_id}",
                ),
                (
                    "Aliexpress",
                    None,
                    "https://www.aliexpress.com/p/order/detail.html?orderId={order_id}",
                    "https://www.aliexpress.com/item/{item_id}.html",
                ),
            ]:
                branch_name = shop[1] if shop[1] else shop[0]
                logo_path = (
                    settings.BASE_DIR / f"logos/{branch_name.lower()}.png"
                )
                logo_img = None
                if os.access(logo_path, os.R_OK):
                    logo_img = File(open(logo_path, "rb"), logo_path.name)

                (shop_object, created) = Shop.objects.update_or_create(
                    name=shop[0],
                    branch_name=branch_name,
                    defaults={
                        "order_url_template": shop[2] if shop[2] else "",
                        "item_url_template": shop[3] if shop[3] else "",
                    },
                )
                if logo_img:
                    if shop_object.icon:
                        shop_object.icon.delete()
                    shop_object.icon = logo_img
                    shop_object.save()
                    logo_img.close()
                if created:
                    self.log.debug("Created new shop: %s", shop_object)
                else:
                    self.log.debug(
                        "Found and possibly updated: %s", shop_object
                    )

    # def command_load_to_db_adafruit(self, options):
    #     if settings.SCRAPER_ADA_DB_SHOP_ID != -1:
    #         self.log.debug("Using db shop ID from SCRAPER_ADA_DB_SHOP_ID")
    #         db_shop_id = int(settings.SCRAPER_ADA_DB_ID)
    #     elif options["db_shop_id"] != -1:
    #         self.log.debug("Using db shop ID from --db-shop-id")
    #         db_shop_id = int(options["db_shop_id"])
    #     else:
    #         self.log.debug(
    #             "No value for db shop ID found, unable to load to db. Need"
    #             " either SCRAPER_ADA_DB_SHOP_ID or --db-shop-id"
    #         )
    #         raise CommandError(
    #             "No value for db shop ID found, unable to load to db."
    #         )
    #     shop = Shop.objects.get(id=db_shop_id)
    #     self.log.debug("Loaded shop from model: %s", shop)

    #     self.log.debug("Loading on-disk data")
    #     for json_file in self.cache["ORDERS"].glob("*/*.json"):
    #         self.log.debug(
    #             "Processing file %s/%s", json_file.parent.name, json_file.name
    #         )
    #         order_dict = self.read(json_file, from_json=True)

    #         for order_id, order in order_dict.items():
    #             items = order["items"].copy()
    #             del order["items"]
    #             date = order["date_purchased"]
    #             del order["date_purchased"]
    #             # self.pprint(items)
    #             prices = {
    #                 "total": Money(0, "USD"),
    #                 "subtotal": Money(0, "USD"),
    #                 "tax": Money(0, "USD"),
    #                 "shipping": Money(0, "USD"),
    #             }
    #             defaults = {
    #                 "date": datetime.fromisoformat(date),
    #                 "extra_data": order,
    #             }
    #             defaults.update(prices)
    #             order_object, created = Order.objects.update_or_create(
    #                 shop=shop,
    #                 order_id=order_id,
    #                 defaults=defaults,
    #             )

    #             for item_id, item in items.items():
    #                 # print(item_id, item)
    #                 name = item["product name"]
    #                 del item["product name"]

    #                 quantity = item["quantity"]
    #                 del item["quantity"]

    #                 thumb_path = self.cache["BASE"] / item["png"]
    #                 thumb_img = File(open(thumb_path, "rb"), thumb_path.name)
    #                 del item["png"]

    #                 # Save html and pdf as attachements
    #                 # del item["html"]
    #                 # del item["pdf"]

    #                 item_object, created = OrderItem.objects.update_or_create(
    #                     order=order_object,
    #                     item_id=item_id,
    #                     item_sku="",  # Adafruit has no SKUs?
    #                     defaults={
    #                         "name": name,
    #                         "count": quantity,
    #                         "extra_data": item,
    #                     },
    #                 )

    #                 if item_object.thumbnail:
    #                     item_object.thumbnail.delete()
    #                 item_object.thumbnail = thumb_img
    #                 item_object.save()

    #                 if thumb_img:
    #                     thumb_img.close()
    #             if created:
    #                 self.log.debug("Created order %s", order_id)
    #             else:
    #                 self.log.debug("Created or updated order %s", order_object)


    # def command_load_to_db_aliexpress(self):
    #     shop = self.get_shop()
    #     self.log.debug("Loaded shop from model: %s", shop)

    #     self.log.debug("Loading on-disk data")
    #     counter = 0
    #     max_title_length = 0

    #     for json_file in self.cache["ORDERS"].glob("*/*.json"):
    #         counter += 1
    #         # self.log.debug(
    #         #    "Processing file %s/%s", json_file.parent.name, json_file.name
    #         # )
    #         order_dict = self.read(json_file, from_json=True)
    #         items = order_dict["items"].copy()
    #         del order_dict["items"]
    #         date = order_dict["date"]
    #         del order_dict["date"]
    #         order_id = order_dict["id"]
    #         del order_dict["id"]

    #         prices = {
    #             "total": Money(0, "USD"),
    #             "subtotal": Money(0, "USD"),
    #             "tax": Money(0, "USD"),
    #             "shipping": Money(0, "USD"),
    #         }
    #         price_items = order_dict["price_items"].copy()
    #         for key in price_items:
    #             value = Price.fromstring(order_dict["price_items"][key])
    #             if value.amount == 0 and not value.currency:
    #                 self.log.debug(
    #                     "Value is 0 and currency in None, forcing to $: %s",
    #                     order_dict["price_items"][key],
    #                 )
    #                 value.currency = "$"
    #             try:
    #                 assert value.currency in ["$", "€"]
    #             except AssertionError as err:
    #                 self.log.debug(
    #                     "Ops, value was %s => %s %s",
    #                     order_dict["price_items"][key],
    #                     value.amount,
    #                     value.currency,
    #                 )
    #                 raise err

    #             if key.lower() in prices.keys():
    #                 prices[key.lower()] = Money(
    #                     value.amount, "USD" if value.currency == "$" else "EUR"
    #                 )
    #                 del order_dict["price_items"][key]

    #         if order_dict["status"] not in ["finished", "closed"]:
    #             self.log.info(
    #                 self.command.style.WARNING(
    #                     "Not loading order %s to DB because status is %s"
    #                 ),
    #                 order_id,
    #                 order_dict["status"],
    #             )
    #             continue

    #         for key, value in items.items():
    #             max_title_length = max(max_title_length, len(value["title"]))
    #             #
    #             if not (
    #                 all(
    #                     [
    #                         (
    #                             self.can_read(
    #                                 self.cache["BASE"] / value["thumbnail"]
    #                             )
    #                         ),
    #                         (
    #                             self.can_read(
    #                                 self.cache["BASE"]
    #                                 / value["snapshot"]["pdf"]
    #                             )
    #                         ),
    #                         (
    #                             self.can_read(
    #                                 self.cache["BASE"]
    #                                 / value["snapshot"]["html"]
    #                             )
    #                         ),
    #                     ]
    #                 )
    #             ):
    #                 self.log.error(
    #                     self.command.style.ERROR(
    #                         "Not importing item %s in order %s because some"
    #                         " files were missing"
    #                     ),
    #                     key,
    #                     order_id,
    #                 )
    #         defaults = {
    #             "date": datetime.fromisoformat(date),
    #             "extra_data": order_dict,
    #         }
    #         defaults.update(prices)

    #         order_object, created = Order.objects.update_or_create(
    #             shop=shop,
    #             order_id=order_id,
    #             defaults=defaults,
    #         )
    #         if created:
    #             self.log.debug(
    #                 self.command.style.SUCCESS("Created order %s"), order_object
    #             )
    #         # else:
    #         #    self.log.debug("Created or updated order %s", order_object)

    #     self.log.info(
    #         "Loaded %s orders. The longest item title was %s characters.",
    #         counter,
    #         max_title_length,
    #     )


    # def get_shop(self, options):
    #     if settings.SCRAPER_ALI_DB_SHOP_ID != -1:
    #         self.log.debug("Using db shop ID from SCRAPER_ALI_DB_SHOP_ID")
    #         shop_id = int(settings.SCRAPER_ALI_DB_SHOP_ID)
    #     elif self.options["db_shop_id"] != -1:
    #         self.log.debug("Using db shop ID from --db-shop-id")
    #         shop_id = int(options["db_shop_id"])
    #     else:
    #         self.log.debug(
    #             "No value for db shop ID found, unable to load to db. Need"
    #             " either SCRAPER_ALI_DB_SHOP_ID or --db-shop-id"
    #         )
    #         raise CommandError(
    #             "No value for db shop ID found, unable to load to db."
    #         )
    #     return Shop.objects.get(id=shop_id)
