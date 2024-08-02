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
from django.core.cache import cache
from django.core.files import File
from djmoney.money import Money

# pylint: disable=relative-beyond-top-level
from hlo.models import Attachment, Order, OrderItem, Shop

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
                    "manual_input": False,
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

                order_id = order["id"]
                del order["id"]

                (order_object, created) = Order.objects.update_or_create(
                    shop=self.shop,
                    order_id=order_id,
                    defaults=defaults,
                )

                if (
                    "attachements" in order  # keep
                    or "attachments" in order
                ):
                    if not options["skip_attachments"]:
                        if "attachments" in order:
                            order_attachments = order["attachments"]
                        else:
                            order_attachments = order[
                                "attachements"  # keep
                            ]
                        existing_sha1s = [
                            x.sha1 for x in order_object.attachments.all()
                        ]
                        for attachment in order_attachments:
                            attachment_path = Path(
                                attachment["path"],
                            ).as_posix()
                            attachment_file = None
                            order_attachment_zip_file = zipp.Path(
                                zip_data,
                                attachment_path,
                            )
                            if order_attachment_zip_file.is_file():
                                attachment_file = File(
                                    order_attachment_zip_file.open("rb"),
                                    attachment_path,
                                )
                            else:
                                msg = (
                                    "Thumbnail "
                                    f"{order_attachment_zip_file.name}"
                                    f" not in {zip_file.name}"
                                )
                                raise AttributeError(msg)
                            sha1hash = hashlib.sha1()  # noqa: S324
                            if attachment_file.multiple_chunks():
                                for chunk in attachment_file.chunks():
                                    sha1hash.update(chunk)
                            else:
                                sha1hash.update(attachment_file.read())

                            sha1 = sha1hash.hexdigest()

                            if (
                                len(existing_sha1s) == 0
                                or sha1 not in existing_sha1s
                            ):
                                defaults = {
                                    "sha1": sha1,
                                    "manual_input": False,
                                }
                                if "name" in attachment:
                                    defaults["name"] = attachment["name"]
                                if "comment" in attachment:
                                    defaults["comment"] = attachment["comment"]

                                self.log.debug(
                                    "Creating Attachment.object for %s (%s)",
                                    attachment_file,
                                    defaults,
                                )

                                (
                                    attachment_object,
                                    created,
                                ) = Attachment.objects.update_or_create(
                                    sha1=sha1,
                                    defaults=defaults,
                                )
                                order_object.attachments.add(
                                    attachment_object,
                                )
                                order_object.save()
                                attachment_object.file = attachment_file
                                attachment_object.save()
                                for key in [
                                    "attachment_count",
                                    "attachment_pdf",
                                    "attachment_html",
                                ]:
                                    cache.delete(key)
                            else:
                                self.log.debug(
                                    "Found hash %s for %s",
                                    sha1,
                                    attachment_path,
                                )
                    if "attachments" in order:
                        del order["attachments"]
                    else:
                        del order["attachements"]  # keep

                del order["date"]

                for item in order["items"]:
                    self.log.debug(
                        "Item ID: %s, Order ID: %s",
                        item["id"],
                        order_id,
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
                        "manual_input": False,
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
                    item_attachments = []
                    if "attachements" in item:  # keep
                        if not options["skip_attachments"]:
                            item_attachments = item["attachements"]  # keep
                        del item["attachements"]  # keep
                    if "attachments" in item:
                        if not options["skip_attachments"]:
                            item_attachments = item["attachments"]
                        del item["attachments"]

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
                            zip_data,
                            Path(item_thumbnail).as_posix(),
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
                        sha1 = ""
                        if item_object.thumbnail_sha1:
                            sha1hash = hashlib.sha1()  # noqa: S324
                            if thumbnail_file.multiple_chunks():
                                for chunk in thumbnail_file.chunks():
                                    sha1hash.update(chunk)
                            else:
                                sha1hash.update(thumbnail_file.read())
                            sha1 = sha1hash.hexdigest()
                        if (
                            not item_object.thumbnail_sha1
                            or item_object.thumbnail_sha1 != sha1
                        ):
                            self.log.debug(
                                "No sha1 or not matching: %s %s",
                                item_object.thumbnail_sha1,
                                sha1,
                            )
                            if item_object.thumbnail:
                                item_object.thumbnail.delete()
                            item_object.thumbnail = thumbnail_file
                            item_object.save()
                            cache.delete("orderitem_count")

                    self.log.debug("Getting existing sha1s")
                    existing_sha1s = [
                        x.sha1 for x in item_object.attachments.all()
                    ]
                    self.log.debug("Got existing sha1s: %s ", existing_sha1s)

                    for attachment in item_attachments:
                        attachment_path = Path(
                            attachment["path"],
                        ).as_posix()
                        attachment_file = None
                        self.log.debug(
                            "Looking for item attachment %s",
                            attachment_path,
                        )
                        attachment_zip_file = zipp.Path(
                            zip_data,
                            attachment_path,
                        )
                        if attachment_zip_file.is_file():
                            attachment_file = File(
                                attachment_zip_file.open("rb"),
                                attachment_path,
                            )
                        else:
                            # Can' understand why it can not find this file
                            # it IS in the file
                            # orders\76061\item-voron-0-2-s1-kit-fra-ldo.pdf
                            # orders\76061\item-voron-0-2-s1-kit-fra-ldo.pdf
                            msg = (
                                f"Attachment {attachment_zip_file.name} "
                                f"({attachment_path} / {attachment['path']})"
                                f" not in {zip_file.name}"
                            )
                            self.log.error(msg)
                            continue
                        sha1hash = hashlib.sha1()  # noqa: S324
                        if attachment_file.multiple_chunks():
                            for chunk in attachment_file.chunks():
                                sha1hash.update(chunk)
                        else:
                            sha1hash.update(attachment_file.read())
                        sha1 = sha1hash.hexdigest()
                        if (
                            len(existing_sha1s) == 0
                            or sha1 not in existing_sha1s
                        ):
                            defaults = {
                                "sha1": sha1,
                                "manual_input": False,
                            }
                            if "name" in attachment:
                                defaults["name"] = attachment["name"]
                            if "comment" in attachment:
                                defaults["comment"] = attachment["comment"]

                            self.log.debug(
                                "Creating Attachment.object for %s (%s)",
                                attachment_file,
                                defaults,
                            )

                            self.log.debug(
                                "Processing %s for text extraction",
                                attachment_file,
                            )
                            if attachment_path.endswith(".pdf"):
                                attachment_zipped_pdf_file = zipp.Path(
                                    zip_data,
                                    attachment_path,
                                )
                                doc = fitz.open(
                                    stream=attachment_zipped_pdf_file.open(
                                        "rb",
                                    ).read(),
                                )
                                text = ""
                                for page in doc:
                                    text += page.get_text()
                                defaults["text"] = text
                            (
                                attachment_object,
                                created,
                            ) = Attachment.objects.update_or_create(
                                sha1=sha1,
                                defaults=defaults,
                            )
                            item_object.attachments.add(attachment_object)
                            item_object.save()
                            attachment_object.file = attachment_file
                            attachment_object.save()
                            for key in [
                                "orderitem_count",
                                "attachment_count",
                                "attachment_pdf",
                                "attachment_html",
                            ]:
                                cache.delete(key)
                        else:
                            self.log.debug(
                                "Found hash %s for %s",
                                sha1,
                                attachment_path,
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
                        "Encountered error when reading %s",
                        path,
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
