import logging

import qrcode
from barcode import Code128
from barcode.writer import ImageWriter
from django.contrib import messages
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from PIL import Image
from qrcode.image.pure import PyPNGImage

from hlo.models import OrderItem

logger = logging.getLogger(__name__)

__all__ = [
    "barcode_render",
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


def barcode_print(_request, pk: int, img_format: str):
    img_format = img_format.lower()
    if img_format not in ["png"]:
        return HttpResponse(status=415)
    orderitem = get_object_or_404(OrderItem, pk=pk)
    url = f"https://bc.h2x.no/{str(orderitem.sha1_id).upper()}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
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
