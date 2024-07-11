from django.http import (
    JsonResponse,
)
from django.views.generic.base import TemplateView


class WebappView(TemplateView):
    template_name = "scan/webapp.html"


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
        status=200,
        content_type="application/json",
    )
