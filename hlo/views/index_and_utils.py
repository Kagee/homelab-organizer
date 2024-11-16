import logging

from django.core.cache import cache
from django.shortcuts import render

from hlo.models import Attachment, OrderItem, StockItem

logger = logging.getLogger(__name__)


# from django.contrib.auth.decorators import user_passes_test
# @user_passes_test(
#    lambda u: u.is_staff,
#    login_url="/do_not_have_access",
#    redirect_field_name=None,
# )


def index(request):
    # This is basically a suboptimal implementation of a
    # (currently non-existing)cache.get_or_set_many
    # with callable support
    keys: dict = {
        "orderitem_count": OrderItem.objects.count,
        "stockitem_count": StockItem.objects.count,
        "attachment_count": Attachment.objects.count,
        "attachment_pdf": Attachment.objects.filter(
            file__endswith=".pdf",
        ).count,
        "attachment_html": Attachment.objects.filter(
            file__endswith=".html",
        ).count,
    }

    cached_keys = cache.get_many(keys.keys())

    for key in keys:
        if key not in cached_keys:
            value = keys[key]()
            cache.set(key, value, timeout=None)
            cached_keys[key] = value

    return render(
        request,
        "common/index.html",
        cached_keys,
    )


def no_access(request):
    return render(request, "no_access.html")


def render404(request, _exception):
    return render(request, "404.html")
