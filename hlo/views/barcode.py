import io
import logging

import qrcode
import requests
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect

from hlo.models import OrderItem

logger = logging.getLogger(__name__)

__all__ = [
    "barcode_render",
    "barcode_print",
    "barcode_redirect",
]


def barcode_render(_request, pk: int, img_format: str):
    img_format = img_format.lower()
    if img_format not in ["png"]:
        return HttpResponse(status=415)
    orderitem = get_object_or_404(OrderItem, pk=pk)
    url = f"https://bc.h2x.no/{str(orderitem.sha1_id).upper()}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=0,
    )

    logger.debug("Url is %s", url)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(
        fill_color="black",
        back_color="white",
    )

    response = HttpResponse(content_type="image/png")
    img.save(response)

    return response


def barcode_print(_request, pk: int):
    if not settings.BQW_ENDPOINT:
        return HttpResponse(
            "Printing not configured on this server", status=501
        )

    orderitem = get_object_or_404(OrderItem, pk=pk)
    qr_url = f"{settings.QR_URL_PREFIX}{str(orderitem.sha1_id).upper()}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=1,
    )

    logger.debug("Url is %s", qr_url)
    qr.add_data(qr_url)
    qr.make(fit=True)

    img = qr.make_image(
        fill_color="black",
        back_color="white",
    )

    response = HttpResponse(content_type="image/png")

    buf = io.BytesIO()
    img.save(buf, format="PNG")

    files = {"image": ("qr-code.png", buf.getvalue(), "image/png")}
    values = {
        "text": "text",  # if we don't have any text, nothing will be printed
        "label_size": "62",
        "orientation": "standard",
        "margin_top": "0",
        "margin_bottom": "0",
        "margin_left": "0",
        "margin_right": "0",
        "print_type": "image",
        "print_count": "1",
        "image_bw_threshold": "70",
        "image_mode": "black_and_white",
        "cut_mode": "cut",
    }

    # post_response = requests.post(
    #    settings.BQW_ENDPOINT, files=files, data=values, timeout=5
    # )
    img.save(response, format="PNG")
    return response


def barcode_redirect(request, barcode: str):
    oi: OrderItem = OrderItem.objects.filter(sha1_id=barcode.lower()).first()
    if not oi:
        messages.add_message(
            request,
            messages.WARNING,
            f"Could not find item with barcode {barcode}.",
        )
        return redirect("index")

    if oi.stockitem.count():
        return redirect("stockitem-detail", pk=oi.stockitem.first().pk)
    return redirect("orderitem", pk=oi.pk)
