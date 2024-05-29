from django.conf import settings
from django.contrib.auth.middleware import PersistentRemoteUserMiddleware


class CustomPersistentRemoteUserMiddleware(PersistentRemoteUserMiddleware):
    header = f"HTTP_{settings.REMOTE_USER_HEADER}".upper().replace("-", "_")
