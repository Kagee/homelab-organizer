import hashlib
import io
import logging
import textwrap
from pathlib import Path
from typing import tuple

import qrcode
import requests
from django.conf import settings
from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from PIL import Image, ImageDraw, ImageFont

from hlo.models import OrderItem

logger = logging.getLogger(__name__)

__all__ = [
    "label_render_orderitem",
    "label_print_orderitem",
    "sha1_redirect",
]


def label_render_orderitem(_request: WSGIRequest, pk: int) -> HttpResponse:
    return _label_response(_get_label(*_orderitem_get_label_data(pk)))


def label_print_orderitem(_request: WSGIRequest, pk: int) -> JsonResponse:
    response = _label_print(_get_label(*_orderitem_get_label_data(pk)))
    """
        $.ajax({
        type : 'POST',
        url :  ...,
        dateType: 'json',
        data: my_data,
        success : function(response){
             ...
        },
        error : function(response, status, error){
            var err = response.responseText;
            alert("Error: " + err);
        }
        });
    """
    if response.ok:
        return JsonResponse({"status": "ok"})
    return JsonResponse(
        {
            "status": "error",
            "status_code": response.status_code,
            "reason": response.reason,
            "text": response.text,
        },
        status_code=500,
    )


def sha1_redirect(request: WSGIRequest, sha1: str) -> HttpResponseRedirect:
    oi: OrderItem = OrderItem.objects.annotate(
        stockitem_count=Count("stockitem"),
    ).get(sha1_id=sha1.lower())
    if not oi:
        # TODO: Add support for sha1 redirect to storage
        messages.add_message(
            request,
            messages.WARNING,
            f"Could not find item with barcode {sha1}.",
        )
        return redirect("index")

    if oi.stockitem_count:
        # There exist a StockItem for this OrderItem, redirect there
        return redirect("stockitem-detail", pk=oi.stockitem.first().pk)
    return redirect("orderitem", pk=oi.pk)


def _orderitem_get_label_data(pk: int) -> tuple(str, str):
    qs = OrderItem.objects.annotate(
        stockitem_count=Count("stockitem"),
    )
    oi = get_object_or_404(qs, pk=pk)
    label_text = oi.name
    if oi.stockitem_count:
        label_text = oi.stockitem.first().stockitem.name
        logger.debug("Making label for text '%s'", label_text)

    label_text = (
        "10/20/30pcs NdFeB Magnet Diametrically Magnetized Rod "
        "Diameter 6x2 mm Experiment Precision Instrumentation Magnets 6*2 mm"
    )
    qr_text = f"{settings.QR_URL_PREFIX}{str(oi.sha1_id).upper()}"
    return qr_text, label_text


def _storage_get_label_data(pk: int) -> tuple(str, str):
    # TODO: Implement
    """
    qs = OrderItem.objects.annotate(
        stockitem_count=Count("stockitem"),
    )
    oi = get_object_or_404(qs, pk=pk)
    label_text = oi.name
    if oi.stockitem_count:
        label_text = oi.stockitem.first().stockitem.name
        logger.debug("Making label for text '%s'", label_text)

    label_text = (
        "10/20/30pcs NdFeB Magnet Diametrically Magnetized Rod "
        "Diameter 6x2 mm Experiment Precision Instrumentation Magnets 6*2 mm"
    )
    qr_text = f"{settings.QR_URL_PREFIX}{str(oi.sha1_id).upper()}"
    """
    label_text = qr_text = pk
    return qr_text, label_text


def _label_response(im: Image) -> HttpResponse:
    response = HttpResponse(content_type="image/png")
    im.save(response, format="PNG")
    return response


def _get_label(qr_text: str, label_text: str) -> Image:
    # get_object_or_404 will do the pk filtering

    font_path = Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")

    label_hash = hashlib.sha1()  # noqa: S324
    label_hash.update(
        (label_text + qr_text + font_path).encode(),  # defaults to utf-8
    )
    hex_hash = label_hash.hexdigest()
    filename = hex_hash[2:] + ".png"
    cache_file: Path = settings.BARCODE_CACHE / hex_hash[:2] / filename
    if cache_file.is_file():
        return Image.open(cache_file)
    return _make_label(label_text, qr_text, cache_file, font_path)


def _label_print(im: Image) -> requests.Response:
    if not settings.BQW_ENDPOINT:
        return HttpResponse(
            "Printing not configured on this server",
            status=501,
        )
    buf = io.BytesIO()
    im.save(buf, format="PNG")

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

    return requests.post(
        settings.BQW_ENDPOINT,
        files=files,
        data=values,
        timeout=5,
    )


def _make_label(
    label_text: str,
    qr_url: str,
    cache_file: Path,
    font_path: Path,
) -> Image:
    im = _make_qr_for_text(qr_url)

    # Make text take ut 3/4 of label width
    text_im = Image.new(
        "RGB",
        size=(im.size[0] * 3, im.size[0]),
        color="white",
    )
    resulting_im = Image.new(
        "RGB",
        size=(im.size[0] * 4, im.size[0]),
        color="white",
    )

    draw = ImageDraw.Draw(text_im)

    def get_reaming_pixels(txt: str, text_im: Image) -> (int, int, int):
        fontsize = 1  # starting font size
        font = ImageFont.truetype(font_path, fontsize)
        _, _, text_width, text_height = draw.textbbox((0, 0), txt, font=font)
        im_width, im_height = text_im.size
        while text_width < im_width and text_height < im_height * 0.95:
            fontsize += 1
            font = ImageFont.truetype(font_path, fontsize)
            _, _, text_width, text_height = draw.textbbox(
                (0, 0),
                txt,
                font=font,
            )

        fontsize -= 1
        font = ImageFont.truetype(font_path, fontsize)
        _, _, text_width, text_height = draw.textbbox((0, 0), txt, font=font)
        return fontsize, text_width, text_height

    im_width, im_height = text_im.size
    best_font_size = -1
    best_breaks = -1
    prev_remainder = -1

    for breaks in range(1, 15):
        try:
            txt = "\n".join(
                textwrap.wrap(label_text, width=len(label_text) / breaks),
            )
        except TypeError:
            # Could not wrap with number of breaks, give up
            break
        fontsize, w, h = get_reaming_pixels(txt, text_im)
        remainder = (im_width * im_height) - (w * h)
        if prev_remainder > -1:
            if remainder < prev_remainder:
                best_font_size = fontsize
                best_breaks = breaks
            else:
                break
        else:
            best_font_size = fontsize
            best_breaks = breaks
        prev_remainder = remainder
        logger.debug(
            "Fontsize: %s (%s, %s), remainder: %s (lower is better)",
            fontsize,
            best_font_size,
            best_breaks,
            remainder,
        )

    font = ImageFont.truetype(font_path, best_font_size)
    txt = "\n".join(
        textwrap.wrap(label_text, width=len(label_text) / best_breaks),
    )
    _, _, text_width, text_height = draw.textbbox((0, 0), txt, font=font)
    draw.text(
        ((im_width - text_width) / 2, (im_height - text_height) / 2),
        txt,
        font=font,
        fill=(0, 0, 0),
    )  # put the text on the image
    resulting_im.paste(im, (0, 0))
    resulting_im.paste(text_im, (im.size[0], 0))

    # Save cache
    cache_file.parent.mkdir(exist_ok=True)
    resulting_im.save(cache_file, format="PNG")

    return resulting_im


def _make_qr_for_text(qr_text: str) -> Image:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    qr.add_data(qr_text)
    qr.make(fit=True)
    return qr.make_image(
        fill_color="black",
        back_color="white",
    ).get_image()