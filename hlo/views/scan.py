import logging
from typing import Any

from django.conf import settings
from django.http import (
    JsonResponse,
)
from django.views.decorators.http import require_http_methods
from django.views.generic.base import TemplateView

from hlo.models import OrderItem, StockItem, Storage, get_object_from_sha1

logger = logging.getLogger(__name__)


class WebappView(TemplateView):
    template_name = "scan/webapp.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        logger.debug(self.request)

        ctx["binaryeye_url"] = (
            # https:// + settings.WEBAPP_DOMAIN + /scan?
            "binaryeye://scan?ret=https%3A%2F%2F"
            + settings.WEBAPP_DOMAIN
            + "%2Fscan%3F"
        )

        if "bec1" in self.request.GET:
            bec1 = self.request.GET["bec1"].split("/")[-1]
            logger.debug("Binary Eye Code 1: %s", bec1)
            if bec1_dict := get_item(bec1):
                logger.debug(bec1_dict)

                # .../scan? + result= + ctx["bec1"] + &result2={RESULT}
                ctx["binaryeye_url"] += "bec1%3D" + bec1 + "%26bec2%3D{RESULT}"

                ctx["bec1"] = bec1_dict
                if "bec2" in self.request.GET:
                    bec2 = self.request.GET["bec2"].split("/")[-1]
                    if bec2 != bec1_dict["sha1"]:
                        logger.debug("Binary Eye Code 2: %s", bec2)
                        if bec2_dict := get_item(bec2):
                            logger.debug(bec2_dict)
                            ctx["bec2"] = bec2_dict
                    else:
                        logger.debug("Binary Eye Code 2 = 1, ignored: %s", bec1)

        else:
            # .../scan? + result={RESULT}
            ctx["binaryeye_url"] += "bec1%3D{RESULT}"

        return ctx


def scan_json_error(msg):
    return JsonResponse(
        {
            "ok": False,
            "result": {
                "msg": msg,
            },
        },
    )


def get_item(sha1: str) -> dict[str, Any] | None:
    """Return object name/type/thumbnail based on SHA1."""
    obj, obj_type = get_object_from_sha1(sha1)

    if not obj:
        return None

    thumbnail = ""
    if isinstance(obj, StockItem):
        thumbnail = obj.thumbnail_url()
    elif isinstance(obj, OrderItem):
        thumbnail = obj.thumbnail.url

    return {
        "name": obj.name,
        "thumbnail": thumbnail,
        "type": obj_type,
        "sha1": sha1,
    }


"""
def get_item2(sha1: str):
    sha1: list[str] = sha1.split("/")
    sha1 = sha1[len(sha1) - 1]
    try:
        orderitem: OrderItem = OrderItem.objects.annotate(
            stockitem_count=Count("stockitems"),
        ).get(sha1_id=sha1.upper())
        if orderitem.stockitem_count:
            return orderitem.stockitems.first()
        return scan_json_error("Order item #{obj.pk} has no stockitem")
    except OrderItem.DoesNotExist:
        try:
            Storage.objects.get(sha1_id=sha1.upper())
        except Storage.DoesNotExist:
            return scan_json_error("No item with that hash exists.")
        return scan_json_error("Scan item first, then storage!")
"""

"""
def get_storage(sha1: str):
    sha1 = sha1.split("/")[-1]
    sha1 = sha1[len(sha1) - 1]
    try:
        return Storage.objects.get(sha1_id=sha1.upper())
    except Storage.DoesNotExist:
        return scan_json_error("No storage with that hash exists.")
"""

"""
@require_http_methods(["POST"])
def move_item_to_storage(request):
    if (code1 := request.POST.get("code1")) and (
        code2 := request.POST.get("code2")
    ):
        logger.debug("move_item_to_storage")
        item = get_item(code1)
        storage = get_storage(code2)

        for o in [item, storage]:
            if isinstance(o, JsonResponse):
                return o

        return JsonResponse(
            {
                "ok": True,
                "result": {
                    "msg": (
                        f"Moving\nItem: {item.name}\n"
                        f"into\nStorage: {storage.name}"
                    ),
                },
            },
        )
    return scan_json_error(
        "Missing item to move or storage to move to",
    )
"""

"""
@require_http_methods(["POST"])
def move_storage_into_storage(request):
    if (code1 := request.POST.get("code1")) and (
        code2 := request.POST.get("code2")
    ):
        logger.debug("move_storage_into_storage")

        child = get_storage(code1)
        parent = get_storage(code2)

        for o in [child, parent]:
            if isinstance(o, JsonResponse):
                return o
        if child == parent:
            return scan_json_error(
                "Can not move item into itself",
            )
        return JsonResponse(
            {
                "ok": True,
                "result": {
                    "msg": (
                        f"Putting\nStorage: {child.name}\n"
                        f"into\nStorage: {parent.name}"
                    ),
                },
            },
        )
    return scan_json_error(
        "Missing storage child and parent",
    )
"""


@require_http_methods(["GET"])
def manifest_json(_request):
    manifest = {
        "name": "HLO Scan",
        "start_url": "scan",
        "display": "standalone",
        "background_color": "#FFFFFF",
        "icons": [
            {
                "src": "static/images/logo/hlo-cc0-logo-black_128.png",
                "sizes": "128x128",
                "type": "image/png",
            },
        ],
    }

    return JsonResponse(
        manifest,
    )
