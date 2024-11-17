import io
import logging
import re
import textwrap
from pathlib import Path

import qrcode  # type: ignore[import-untyped]
import requests
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import redirect
from django.utils.cache import patch_cache_control
from PIL import Image, ImageDraw, ImageFont
from PIL.Image import Image as ImageType

from hlo.models import (
    OrderItem,
    StockItem,
    Storage,
    get_object_from_sha1,
)

logger = logging.getLogger(__name__)

__all__ = [
    "sha1_redirect",
    "label_render_sha1_size",
    "label_print_sha1_size",
]

# At label widths multiplied by more than
# 12, the QR ode is unclear when printing.
MAX_SENSIBLE_LABEL_MULTIPLIER = 12


def label_render_sha1_size(
    _request: WSGIRequest,
    sha1: str,
    multiplier: int,
) -> HttpResponse:
    """Return image with QR and label or HTTP404.

    The larger the multiplier, the smaller the QR code
    will become, because the label width is QR code width * multiplier
    """
    sha1 = sha1.upper()

    if len(sha1) != 40 or not re.match("^[A-Fa-f0-9]*$", sha1):  # noqa: PLR2004
        return HttpResponseBadRequest("Hash is invalid")

    if multiplier < 1 or multiplier > MAX_SENSIBLE_LABEL_MULTIPLIER:
        return HttpResponse(
            (
                f"multiplier must be > 1, < "
                f"{MAX_SENSIBLE_LABEL_MULTIPLIER}, was {multiplier}"
            ),
            status=400,
        )

    filename = sha1[2:] + "_" + str(multiplier) + ".png"

    cache_file: Path = settings.BARCODE_CACHE / sha1[:2] / filename

    if cache_file.is_file():
        logger.debug(
            "Used cached label image: %s/%s",
            cache_file.parent.name,
            cache_file.name,
        )
        return _nocache_png_response(Image.open(cache_file))

    obj, _obj_type = get_object_from_sha1(sha1)
    if not obj:
        return HttpResponseNotFound(f"No object with SHA1 {sha1} found.")

    qr_data, label_text = _obj_get_label_data(obj)
    img = _get_label_size(qr_data, label_text, multiplier)

    # Save cache image
    cache_file.parent.mkdir(exist_ok=True)
    img.save(cache_file, format="PNG")

    return _nocache_png_response(img)


def label_print_sha1_size(
    _request: WSGIRequest,
    sha1: str,
    multiplier: int,
) -> JsonResponse:
    """Print image with QR and label and return status.

    The larger the multiplier, the smaller the QR code
    will become, because the label width is QR code width * multiplier
    """
    if multiplier < 1:
        return JsonResponse(
            {
                "status": "error",
                "reason": f"multiplier must be larger than 1, was {multiplier}",
            },
            status=400,
        )

    obj, obj_type = get_object_from_sha1(sha1)
    if not obj:
        return JsonResponse(
            {
                "status": "error",
                "reason": f"No object with SHA1 {sha1} found.",
            },
            status=400,
        )

    qr_data, label_text = _obj_get_label_data(obj)
    img = _get_label_size(qr_data, label_text, multiplier)

    response: requests.Response
    try:
        response = _label_print(img)
        if response.ok:
            if isinstance(obj, StockItem | Storage):
                obj.label_printed = True  # type: ignore[assignment]
                obj.save()
            else:
                return JsonResponse(
                    {
                        "status": "error",
                        "text": f"Unexpected object type for label: {obj_type}",
                    },
                    status=500,
                )
            return JsonResponse({"status": "ok"})
        return JsonResponse(
            {
                "status": "error",
                "status_code": response.status_code,
                "reason": response.reason,
                "text": response.text,
            },
            status=500,
        )
    except ValueError as ve:
        return JsonResponse(
            {
                "status": "error",
                "text": str(ve),
            },
            status=500,
        )


def _obj_get_label_data(
    obj: OrderItem | StockItem | Storage,
) -> tuple[str, str]:
    """Return QR data(str) and label based on object."""
    label_text = obj.name
    qr_data = f"{settings.QR_URL_PREFIX}{str(obj.sha1_id).upper()}"
    return qr_data, label_text


def _get_label_size(
    qr_text: str,
    label_text: str,
    multiplier: int,
) -> ImageType:
    font_path = Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")

    return _make_label(label_text, qr_text, font_path, multiplier)


def _make_qr_for_text(qr_text: str) -> ImageType:
    """Return QR Image for text."""
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


def _make_label(
    label_text: str,
    qr_url: str,
    font_path: Path,
    multiplier: int,
) -> ImageType:
    im = _make_qr_for_text(qr_url)

    # Make text take ut 3/4 of label width
    text_im = Image.new(
        "RGB",
        size=(im.size[0] * 3, im.size[0]),
        color="white",
    )
    resulting_im = Image.new(
        "RGB",
        size=(im.size[0] * multiplier, im.size[0]),
        color="white",
    )

    draw = ImageDraw.Draw(text_im)

    def get_reaming_pixels(
        txt: str,
        text_im: ImageType,
    ) -> tuple[float, float, float]:
        font_size = 1  # starting font size
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_width, text_height = draw.textbbox((0, 0), txt, font=font)
        im_width, im_height = text_im.size
        while text_width < im_width and text_height < im_height * 0.95:
            font_size += 1
            font = ImageFont.truetype(font_path, font_size)
            _, _, text_width, text_height = draw.textbbox(
                (0, 0),
                txt,
                font=font,
            )

        font_size -= 1
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_width, text_height = draw.textbbox((0, 0), txt, font=font)
        return font_size, text_width, text_height

    im_width, im_height = text_im.size
    best_font_size: float = -1
    best_breaks = -1
    prev_remainder: float = -1

    for breaks in range(1, 15):
        try:
            txt = "\n".join(
                textwrap.wrap(label_text, width=int(len(label_text) / breaks)),
            )
        except TypeError:
            # Could not wrap with number of breaks, give up
            break
        font_size, w, h = get_reaming_pixels(txt, text_im)
        remainder: float = (im_width * im_height) - (w * h)
        if prev_remainder > -1:
            if remainder < prev_remainder:
                best_font_size = font_size
                best_breaks = breaks
            else:
                break
        else:
            best_font_size = font_size
            best_breaks = breaks
        prev_remainder = remainder

    font = ImageFont.truetype(font_path, best_font_size)
    txt = "\n".join(
        textwrap.wrap(label_text, width=int(len(label_text) / best_breaks)),
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

    return resulting_im


def sha1_redirect(
    _request: WSGIRequest,
    sha1: str,
) -> HttpResponseRedirect | HttpResponseNotFound:
    sha1 = sha1.upper()
    obj, _obj_type = get_object_from_sha1(sha1)
    if not obj:
        return HttpResponseNotFound(f"No object with SHA1 {sha1} found.")
    return redirect(obj)


def _nocache_png_response(im: ImageType) -> HttpResponse:
    response = HttpResponse(content_type="image/png")
    patch_cache_control(
        response,
        no_cache=True,
        no_store=True,
        must_revalidate=True,
    )
    im.save(response, format="PNG")  # type: ignore[arg-type]
    return response


def _label_print(im: ImageType) -> requests.Response:
    if not settings.BQW_ENDPOINT:
        msg = "A printer endpoint is not configured"
        raise ValueError(msg)

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
