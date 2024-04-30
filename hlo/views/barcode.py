import logging

from barcode import EAN13
from barcode.writer import ImageWriter
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect

from hlo.models import OrderItem

logger = logging.getLogger(__name__)

__all__ = [
    "barcode_render",
    "barcode_redirect",
]


def barcode_render(request, orderitem):
    # img = Image.new("RGB", (300, 300), "#FFFFFF")
    # data = [(i, randint(100, 200)) for i in range(0, 300, 10)]
    # draw = ImageDraw.Draw(img)
    # draw.polygon(data, fill="#000000")
    response = HttpResponse(mimetype="image/png")
    EAN13(str(orderitem), writer=ImageWriter()).write(response)
    # img.save(response, "PNG")

    return response


def barcode_redirect(request, barcode: str):
    oi: OrderItem = OrderItem.objects.filter(sha1_id=barcode).first()
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
