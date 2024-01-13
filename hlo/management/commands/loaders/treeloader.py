import json
import logging
import os
import zipfile

from django.conf import settings
from django.core.files import File

from hlo.models import Category, Project, Storage


class TreeLoader:
    @classmethod
    def init(cls, input_path, c: Category|Project|Storage):
        log = logging.getLogger(__name__)
        log.debug("Initializing database with projects")
        log.debug("Input file is %s", input_path)
        if not input_path.is_file():
            msg = f"Input file does not exists: {input_path}"
            raise ValueError(msg)

        def rec_item(item, parent):
            print(item["name"])  # noqa: T201
            for child_item in item["children"]:
                rec_item(child_item, None)

        with input_path.open(encoding="utf-8") as input_handle:
            item_list = json.load(input_handle)
            print(c.objects.all())  # noqa: T201
            for root_cat in item_list:
                rec_item(root_cat, None)

        return
        (shop_object, created) = Shop.objects.update_or_create(
            name=shop["name"],
            branch_name=shop["branch_name"],
            defaults={
                "order_url_template": shop["order_url"],  # required
                "item_url_template": shop["item_url"],  # required
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
                        logo_file.open("rb"), f'{shop["name"]}.png',
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
    def init_categories(cls):
        cls.init(settings.INPUT_FOLDER / "hlo_categories.json", Category)


    @classmethod
    def init_projects(cls):
        cls.init(settings.INPUT_FOLDER / "hlo_projects.json", Project)


    @classmethod
    def init_storage(cls):
        cls.init(settings.INPUT_FOLDER / "hlo_storage.json", Storage)
