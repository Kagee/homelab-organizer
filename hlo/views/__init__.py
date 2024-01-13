import logging

from django.shortcuts import render

from hlo.models import Attachement, OrderItem, StockItem

from .category import *
from .orderitems import *
from .orders import *
from .project import *
from .search import *
from .stockitems import *
from .storage import *

logger = logging.getLogger(__name__)


def index(request):
    return render(
        request,
        "index.html",
        {
            "orderitem_count": OrderItem.objects.count(),
            "stockitem_count": StockItem.objects.count(),
            "stockitem_with_location": 0,
            "stockitem_without_location": 0,
            "attachement_count": Attachement.objects.count(),
            "attachement_pdf": Attachement.objects.filter(
                file__endswith=".pdf",
            ).count(),
            "attachement_html": Attachement.objects.filter(
                file__endswith=".html",
            ).count(),
        },
    )


def render404(request, _exception):
    return render(request, "404.html")
