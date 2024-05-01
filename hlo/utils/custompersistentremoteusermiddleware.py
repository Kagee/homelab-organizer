from django.contrib.auth.middleware import PersistentRemoteUserMiddleware


class CustomPersistentRemoteUserMiddleware(PersistentRemoteUserMiddleware):
    header = "HTTP_X_REMOTE_USER"
