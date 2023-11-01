import logging
import os
import sys
from pathlib import Path
import json
import zipfile
from jsonschema import ValidationError, validate
from django.conf import settings
from django.core.files import File
from typing import Any, Dict, List, Union
import pprint
from logging import Logger
from pathlib import Path
from djmoney.money import Money
from decimal import Decimal
import hashlib

# pylint: disable=relative-beyond-top-level
from ....models import Shop, Order, OrderItem


class ShopOrderLoader(object):
    def __init__(self, shop, options):
        self.log = logging.getLogger(__name__)
        self.options = options
        shop_dict = self.read(
            settings.INPUT_FOLDER / f"{shop}.json", from_json=True
        )
        try:
            self.shop = Shop.objects.get(
                name=shop_dict["metadata"]["name"],
                branch_name=shop_dict["metadata"]["branch_name"],
            )
        except Shop.DoesNotExist:
            self.log.critical(
                "Shop '%s' is not in database, did you run --init-shops?", shop
            )
            sys.exit(1)
        # self.pprint(shop_dict["orders"][0])
        order = shop_dict["orders"][0]
        for order in shop_dict["orders"]:
            defaults = {
                "date": order["date"],
            }
            if "extra_data" in order:
                defaults["extra_data"] = order["extra_data"]
                del order["extra_data"]
            for money in ["total", "subtotal", "tax", "shipping"]:
                if money in order:
                    if "currency" not in order[money]:
                        order[money]["currency"] = "NOK"
                    defaults[money] = Money(
                        amount=order[money]["value"],
                        currency=order[money]["currency"],
                    )
                    del order[money]

            # self.log.debug("Defaults are: %s", defaults)
            (order_object, created) = Order.objects.update_or_create(
                shop=self.shop, order_id=order["id"], defaults=defaults
            )

            del order["id"]
            del order["date"]

            for item in order["items"]:
                self.log.debug("Order ID: %s", item["id"])
                if "attachements" in item:
                    # TODO
                    del item["attachements"]
                if "thumbnail" in item:
                    # TODO
                    del item["thumbnail"]
                # self.pprint(item)
                item_variation = ""
                if "variation" in item:
                    item_variation = item["variation"]
                    del item["variation"]
                item_id = item["id"]
                del item["id"]

                defaults = {
                    "name": item["name"],
                    "count": item["quantity"],
                }
                del item["name"]
                del item["quantity"]

                if "extra_data" in item:
                    defaults["extra_data"] = item["extra_data"]
                    del item["extra_data"]
                for money in ["total", "subtotal", "tax", "vat"]:
                    if money in item:
                        if "currency" not in item[money]:
                            item[money]["currency"] = "NOK"
                        if money == "vat":
                            item["tax"] = item["vat"]
                            del item["vat"]
                            money = "tax"
                        data = item[money]
                        defaults[money] = Money(
                            amount=data["value"], currency=data["currency"]
                        )
                        del item[money]

                assert item == {}, item
                (item_object, created) = OrderItem.objects.update_or_create(
                    item_id=item_id,
                    item_variation=item_variation,
                    order=order_object,
                    defaults=defaults,
                )
                self.log.debug(
                    "Item %s %s", item_object, "created" if created else "found"
                )

            del order["items"]

            assert order == {}, order
            if created:
                self.log.debug("Order was just created")

            self.log.debug(order_object)

    def read(
        self,
        path: Union[Path, str],
        from_json=False,
        **kwargs,
    ) -> Any:
        with open(path, "r", encoding="utf-8-sig") as file:
            contents: str = file.read()
            if from_json:
                try:
                    contents = json.loads(contents)
                except json.decoder.JSONDecodeError as jde:
                    self.log.error("Encountered error when reading %s", path)
                    raise IOError(
                        f"Encountered error when reading {path}", jde
                    ) from jde
            return contents

    @classmethod
    def pprint(cls, value: Any) -> None:
        pprint.PrettyPrinter(indent=2).pprint(value)

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
