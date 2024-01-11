import logging
from django.shortcuts import render

# pylint: disable=wildcard-import,unused-wildcard-import
from .search import *
from .orders import *
from .orderitems import *
from .stockitems import *
from .storage import *
from .project import *
from .category import *

from hlo.models import *

logger = logging.getLogger(__name__)


# Create your views here.
def index(request):
    # count stuff here
    # order_count = 0
    return render(
        request, "index.html", {
            "orderitem_count": OrderItem.objects.count(),
            "stockitem_count": StockItem.objects.count(),
            "stockitem_with_location": 0,
            "stockitem_without_location": 0,
            "attachement_count": Attachement.objects.count(),
            "attachement_pdf": Attachement.objects.filter(file__endswith=".pdf").count(),
            "attachement_html": Attachement.objects.filter(file__endswith=".html").count(),
            }
    )

def render404(request, exception):
     return render(
        request, "404.html"
    )
