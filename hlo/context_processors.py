from django.conf import settings


def global_template_vars(_request):
    return {"LOGOUT_URL": settings.LOGOUT_URL or ""}
