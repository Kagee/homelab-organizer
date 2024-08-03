import json
import logging
import os
import zipfile
from pathlib import Path  # noqa: TCH003

from django.conf import settings
from django.core.files import File
from jsonschema import ValidationError, validate

# pylint: disable=relative-beyond-top-level
from hlo.models import Shop


class ShopMetaLoader:
    @classmethod
    def load(cls) -> None:
        log = logging.getLogger(__name__)
        log.debug("Initializing database with shops")
        log.debug("Input folder is %s", settings.INPUT_FOLDER)

        json_file: Path
        for json_file in settings.INPUT_FOLDER.glob("*.json"):
            if not os.access(json_file, os.R_OK):
                log.error("Could not open/read %s", json_file)
                continue

            with json_file.open(encoding="utf-8") as json_file_handle:
                json_data = json.load(json_file_handle)
                if cls.valid_json(json_data):
                    log.debug("Valid schema in %s", json_file.name)
                else:
                    log.error("Invalid schema in %s", json_file.name)
                    continue

            shop = json_data["metadata"]

            (shop_object, created) = Shop.objects.update_or_create(
                name=shop["name"],
                branch_name=shop["branch_name"],
                defaults={
                    "order_url_template": shop["order_url"],  # required
                    "item_url_template": shop["item_url"],  # required
                    "manual_input": False,
                },
            )
            zip_file = json_file.with_suffix(".zip")
            if not os.access(zip_file, os.R_OK):
                # For now, ZIP files are required, even if empty
                log.warning("Could not open/read %s", zip_file)
            else:
                with zipfile.ZipFile(zip_file) as zip_data:
                    logo_file = zipfile.Path(zip_data, "logo.png")
                    logo_img = None
                    if logo_file.is_file():
                        logo_img = File(
                            logo_file.open("rb"),
                            f'{shop["name"]}.png',
                        )
                    else:
                        log.debug("No %s in %s", logo_file.name, zip_file.name)

                    if logo_img:
                        if shop_object.icon:
                            shop_object.icon.delete()
                        shop_object.icon = logo_img
                        shop_object.save()
                        logo_img.close()
            if created:
                log.info("Created new shop: %s", shop_object.branch_name)
            else:
                log.info(
                    "Found and possibly updated: %s",
                    shop_object.branch_name,
                )

    @classmethod
    def valid_json(cls, structure):
        log = logging.getLogger(__name__)
        with settings.JSON_SCHEMA.open(encoding="utf-8") as schema_file:
            schema = json.load(schema_file)
            try:
                validate(instance=structure, schema=schema)
            except ValidationError as vde:
                log.warning(
                    "JSON failed validation: %s at %s",
                    vde.message,
                    vde.json_path,
                )
                for deprecated in settings.JSON_SCHEMAS_DEPRECATED:
                    schema_file_path = Path(deprecated).resolve()
                    with schema_file_path.open(
                        encoding="utf-8"
                    ) as schema_file_deprecated:
                        schema = json.load(schema_file_deprecated)
                        try:
                            validate(instance=structure, schema=schema)

                        except ValidationError as vde:
                            pass
                        else:
                            log.warning(
                                "Validated using deprecated schema: %s",
                                schema_file_path.name,
                            )
                            return True
                return False
        return True
