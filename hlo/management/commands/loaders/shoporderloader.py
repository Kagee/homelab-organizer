import hashlib
import json
import logging
import pprint
import sys
import zipfile
from pathlib import Path
from typing import Any

import fitz
import zipp
from django.conf import settings
from django.core.files import File
from djmoney.money import Money

# pylint: disable=relative-beyond-top-level
from hlo.models import Attachement, Order, OrderItem, Shop

# Get an instance of a logger
logger = logging.getLogger(__name__)


class ShopOrderLoader:
    def __init__(self, shop, options):  # noqa: C901, PLR0915
        self.log = logging.getLogger(__name__)
        self.options = options
        json_file: Path = settings.INPUT_FOLDER / f"{shop}.json"
        shop_dict = self.read(
            json_file,
            from_json=True,
        )

        zip_file = json_file.with_suffix(".zip")

        try:
            self.shop = Shop.objects.get(
                name=shop_dict["metadata"]["name"],
                branch_name=shop_dict["metadata"]["branch_name"],
            )
        except Shop.DoesNotExist:
            self.log.critical(
                "Shop '%s' is not in database, did you run --init-shops?",
                shop,
            )
            sys.exit(1)
        self.log.debug("Working with .zip file %s", zip_file)
        with zipfile.ZipFile(zip_file) as zip_data:
            order = shop_dict["orders"][0]
            for order in shop_dict["orders"]:
                if all(float(x["quantity"]) < 0 for x in order["items"]):
                    self.log.debug(
                        "Skipping order id %s because "
                        "all items have negative quantity",
                    )
                    continue
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

                # self.log.debug("Defaults are: %s", defaults)i
                order_id = order["id"]
                del order["id"]
                (order_object, created) = Order.objects.update_or_create(
                    shop=self.shop,
                    order_id=order_id,
                    defaults=defaults,
                )

                if "attachements" in order:
                    if not options["skip_attachements"]:
                        order_attachements = order["attachements"]
                        existing_sha1s = [
                            x.sha1 for x in order_object.attachements.all()
                        ]
                        for attachement in order_attachements:
                            attachement_path = Path(
                                attachement["path"],
                            ).as_posix()
                            attachement_file = None
                            order_attachement_zip_file = zipp.Path(
                                zip_data, attachement_path,
                            )
                            if order_attachement_zip_file.is_file():
                                self.log.debug("Is file %s", attachement_path)
                                attachement_file = File(
                                    order_attachement_zip_file.open("rb"),
                                    attachement_path,
                                )
                            else:
                                msg = f"Thumbnail {
                                    order_attachement_zip_file.name
                                    } not in {zip_file.name}"
                                raise AttributeError(msg)
                            sha1hash = hashlib.sha1()  # noqa: S324
                            if attachement_file.multiple_chunks():
                                for chunk in attachement_file.chunks():
                                    sha1hash.update(chunk)
                            else:
                                sha1hash.update(attachement_file.read())

                            sha1 = sha1hash.hexdigest()

                            if (
                                len(existing_sha1s) == 0
                                or sha1 not in existing_sha1s
                            ):
                                defaults = {
                                    "sha1": sha1,
                                }
                                if "name" in attachement:
                                    defaults["name"] = attachement["name"]
                                if "comment" in attachement:
                                    defaults["comment"] = attachement["comment"]

                                self.log.debug(
                                    "Creating Attachement.object for %s (%s)",
                                    attachement_file,
                                    defaults,
                                )

                                (
                                    attachement_object,
                                    created,
                                ) = Attachement.objects.update_or_create(
                                    sha1=sha1,
                                    defaults=defaults,
                                )
                                order_object.attachements.add(
                                    attachement_object,
                                )
                                order_object.save()
                                attachement_object.file = attachement_file
                                attachement_object.save()
                            else:
                                self.log.debug(
                                    "Found hash %s for %s",
                                    sha1,
                                    attachement_path,
                                )
                    del order["attachements"]

                del order["date"]

                for item in order["items"]:
                    self.log.debug(
                        "Item ID: %s, Order ID: %s", item["id"], order_id,
                    )
                    if float(item["quantity"]) < 0:
                        self.log.debug(
                            "Skipping item ID: %s, "
                            "order ID: %s because "
                            "quantity is %s",
                            item["id"],
                            order_id,
                            float(item["quantity"]),
                        )
                        continue
                    item_variation = ""
                    if "variation" in item:
                        item_variation = item["variation"]
                        del item["variation"]
                    item_id = item["id"]
                    del item["id"]

                    defaults = {
                        "name": item["name"],
                        "count": item["quantity"],
                        "item_id": item_id,
                        "item_variation": item_variation,
                        "order": order_object,
                    }
                    del item["name"]
                    del item["quantity"]

                    if "extra_data" in item:
                        defaults["extra_data"] = item["extra_data"]
                        del item["extra_data"]
                    for money in ["total", "subtotal", "tax", "vat"]:
                        money_in_loop = money
                        if money_in_loop in item:
                            if "currency" not in item[money_in_loop]:
                                item[money_in_loop]["currency"] = "NOK"
                            if money_in_loop == "vat":
                                item["tax"] = item["vat"]
                                del item["vat"]
                                money_in_loop = "tax"
                            data = item[money_in_loop]
                            defaults[money_in_loop] = Money(
                                amount=data["value"],
                                currency=data["currency"],
                            )
                            del item[money_in_loop]
                    item_thumbnail = None
                    if "thumbnail" in item:
                        item_thumbnail = item["thumbnail"]
                        del item["thumbnail"]
                    item_attachements = []
                    if "attachements" in item:
                        if not options["skip_attachements"]:
                            item_attachements = item["attachements"]
                        del item["attachements"]

                    if item != {}:
                        msg = f"Item object not empty: {item}"
                        raise ValueError(msg)
                    (item_object, created) = OrderItem.objects.update_or_create(
                        item_id=item_id,
                        item_variation=item_variation,
                        order=order_object,
                        defaults=defaults,
                    )

                    if item_thumbnail:
                        thumbnail_file = None
                        thumbnail_zip_file = zipp.Path(
                            zip_data, Path(item_thumbnail).as_posix(),
                        )
                        if thumbnail_zip_file.is_file():
                            thumbnail_file = File(
                                thumbnail_zip_file.open("rb"),
                                Path(item_thumbnail).as_posix(),
                            )
                        else:
                            msg = (
                                f"Thumbnail {thumbnail_zip_file.name}"
                                f" not in {zip_file.name}"
                            )
                            raise AttributeError(msg)
                        sha1 = None
                        if item_object.sha1:
                            sha1hash = hashlib.sha1()  # noqa: S324
                            if thumbnail_file.multiple_chunks():
                                for chunk in thumbnail_file.chunks():
                                    sha1hash.update(chunk)
                            else:
                                sha1hash.update(thumbnail_file.read())
                            sha1 = sha1hash.hexdigest()
                        if not item_object.sha1 or item_object.sha1 != sha1:
                            self.log.debug(
                                "No sha1 or not matching: %s %s",
                                item_object.sha1,
                                sha1,
                            )
                            if item_object.thumbnail:
                                item_object.thumbnail.delete()
                            item_object.thumbnail = thumbnail_file
                            item_object.save()

                    self.log.debug("Getting existing sha1s")
                    existing_sha1s = [
                        x.sha1 for x in item_object.attachements.all()
                    ]
                    self.log.debug("Got existing sha1s: %s ", existing_sha1s)

                    for attachement in item_attachements:
                        attachement_path = Path(attachement["path"]).as_posix()
                        attachement_file = None
                        self.log.debug(
                            "Looking for item attachement %s",
                            attachement_path,
                        )
                        attachement_zip_file = zipp.Path(
                            zip_data, attachement_path,
                        )
                        if attachement_zip_file.is_file():
                            attachement_file = File(
                                attachement_zip_file.open("rb"),
                                attachement_path,
                            )
                        else:
                            msg = (
                                f"Attachement {attachement_zip_file.name}"
                                f" not in {zip_file.name}"
                            )
                            raise AttributeError(msg)
                        sha1hash = hashlib.sha1()  # noqa: S324
                        if attachement_file.multiple_chunks():
                            for chunk in attachement_file.chunks():
                                sha1hash.update(chunk)
                        else:
                            sha1hash.update(attachement_file.read())
                        sha1 = sha1hash.hexdigest()
                        if (
                            len(existing_sha1s) == 0
                            or sha1 not in existing_sha1s
                        ):
                            defaults = {
                                "sha1": sha1,
                            }
                            if "name" in attachement:
                                defaults["name"] = attachement["name"]
                            if "comment" in attachement:
                                defaults["comment"] = attachement["comment"]

                            self.log.debug(
                                "Creating Attachement.object for %s (%s)",
                                attachement_file,
                                defaults,
                            )

                            self.log.debug(
                                "Processing %s for text extraction",
                                attachement_file,
                            )
                            if attachement_path.endswith(".pdf"):
                                attachement_ziped_pdf_file = zipp.Path(
                                    zip_data, attachement_path,
                                )
                                doc = fitz.open(
                                    stream=attachement_ziped_pdf_file.open(
                                        "rb",
                                    ).read(),
                                )
                                text = ""
                                for page in doc:
                                    text += page.get_text()
                                defaults["text"] = text
                            (
                                attachement_object,
                                created,
                            ) = Attachement.objects.update_or_create(
                                sha1=sha1,
                                defaults=defaults,
                            )
                            item_object.attachements.add(attachement_object)
                            item_object.save()
                            attachement_object.file = attachement_file
                            attachement_object.save()
                        else:
                            self.log.debug(
                                "Found hash %s for %s", sha1, attachement_path,
                            )
                    self.log.debug(
                        "Item %s %s",
                        item_object,
                        "created" if created else "found",
                    )

                del order["items"]

                if order != {}:
                    msg = f"order object is not empty: {order}"
                    raise ValueError(msg)
                if created:
                    self.log.debug("Order was just created")

    def read(
        self,
        path: Path | str,
        *,
        from_json=False,
        **_kwargs,
    ) -> Any:
        with path.open(encoding="utf-8-sig") as file:
            contents: str = file.read()
            if from_json:
                try:
                    contents = json.loads(contents)
                except json.decoder.JSONDecodeError as jde:
                    self.log.exception(
                        "Encountered error when reading %s", path,
                    )
                    msg = f"Encountered error when reading {path}"
                    raise OSError(
                        msg,
                        jde,
                    ) from jde
            return contents

    @classmethod
    def pprint(cls, value: Any) -> None:
        pprint.PrettyPrinter(indent=2).pprint(value)
