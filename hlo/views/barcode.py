import logging

from django.contrib import messages
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import redirect, render

logger = logging.getLogger(__name__)


def chart(request):
    img = Image.new("RGB", (300, 300), "#FFFFFF")
    data = [(i, randint(100, 200)) for i in range(0, 300, 10)]
    draw = ImageDraw.Draw(img)
    draw.polygon(data, fill="#000000")
    response = HttpResponse(mimetype="image/png")
    img.save(response, "PNG")
    return response
