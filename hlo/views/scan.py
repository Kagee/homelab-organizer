import logging

from django.db.models import Count
from django.http import (
    JsonResponse,
)
from django.views.decorators.http import require_http_methods
from django.views.generic.base import TemplateView

from hlo.models import OrderItem, StockItem, Storage

logger = logging.getLogger(__name__)


class WebappView(TemplateView):
    template_name = "scan/webapp.html"


def scan_json_error(msg):
    return JsonResponse(
        {
            "ok": False,
            "result": {
                "msg": msg,
            },
        },
    )


def get_item(sha1: str):
    sha1 = sha1.split("/")
    sha1 = sha1[len(sha1) - 1]
    try:
        orderitem: OrderItem = OrderItem.objects.annotate(
            stockitem_count=Count("stockitems"),
        ).get(sha1_id=sha1.upper())
        if orderitem.stockitem_count:
            stockitem = orderitem.stockitems.first()
            return stockitem
        # return orderitem
        return scan_json_error("Order item #{obj.pk} has no stockitem")
    except OrderItem.DoesNotExist:
        try:
            Storage.objects.get(sha1_id=sha1.upper())
        except Storage.DoesNotExist:
            return scan_json_error("No item with that hash exists.")
        return scan_json_error("Scan item first, then storage!")


def get_storage(sha1: str):
    sha1 = sha1.split("/")
    sha1 = sha1[len(sha1) - 1]
    try:
        return Storage.objects.get(sha1_id=sha1.upper())
    except Storage.DoesNotExist:
        return scan_json_error("No storage with that hash exists.")


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
                    )
                },
            },
        )
    return scan_json_error(
        "Missing storage child and parent",
    )


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
