"""Django settings for hlo project."""

from pathlib import Path
from typing import Any

import environ

from hlo.utils.colored_logs import ColoredLogFormatter

env = environ.FileAwareEnv(
    # set casting, default value
    HLO_DEBUG=(bool, False),
    HLO_ALLOWED_HOSTS=(list, []),
    # https://docs.djangoproject.com/en/3.2/topics/i18n/
    HLO_LANGUAGE_CODE=(str, "nb"),
    HLO_TIME_ZONE=(str, "UTC"),
    HLO_USE_I18N=(bool, False),
    HLO_USE_L10N=(bool, False),
    HLO_USE_TZ=(bool, True),
    # https://docs.djangoproject.com/en/3.2/howto/static-files/
    HLO_STATIC_URL=(str, "/static/"),
    HLO_PASSWORD_MIN_LEN=(int, 14),
)

env.prefix = "HLO_"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

MEDIA_ROOT: Path = (BASE_DIR / Path("media_root")).resolve()
MEDIA_URL: str = "files/"
# Take environment variables from .env file

PROD: bool = env("PROD", default=False)

env_file = ".env-prod" if PROD else ".env"

env.read_env(BASE_DIR / env_file)

DEBUG: bool = env("DEBUG", default=False)

INTERNAL_IPS = [
    "127.0.0.1",
]

INTERNAL_IPS += env.list("INTERNAL_IPS", default=[])

LANGUAGE_CODE: str = env("LANGUAGE_CODE")
TIME_ZONE: str = env("TIME_ZONE")
USE_I18N: bool = env("USE_I18N")
USE_L10N: bool = env("USE_L10N")
USE_TZ: bool = env("USE_TZ")

DATE_FORMAT = "Y-m-d"

# Raises Django's ImproperlyConfigured
# exception if SECRET_KEY not in os.environ
SECRET_KEY: str = env("SECRET_KEY")

# Parse database connection url strings


SQLITE3_FILE: str = env("SQLITE3_FILE", default="")

if SQLITE3_FILE:
    DATABASES = {
        "default": {
            "ENGINE": "hlo.sqlite3",
            "NAME": BASE_DIR / SQLITE3_FILE,
        },
    }
else:
    DATABASES = {
        # read os.environ['DATABASE_URL'] and raises
        # ImproperlyConfigured exception if not found
        "default": env.db(),
    }


# Override this in logging.py
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "V: {asctime} [{levelname}] {message} ({name}:{module})",
            "style": "{",
        },
        "simple": {
            "format": "S: {levelname} {message}",
            "style": "{",
        },
        "coloredlogs": {
            "()": lambda: ColoredLogFormatter(
                fmt=("{asctime} [{levelname[0]}] {message} ({name})"),
                style="{",
            ),
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        # "file": {
        #    "class": "logging.FileHandler",
        #    "filename": "hlo.log",
        #    "formatter": "verbose",
        #    "encoding": "utf-8",
        # },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}

ALLOWED_HOSTS: list[str] = env.list("ALLOWED_HOSTS")

CSRF_TRUSTED_ORIGINS: list[str] = env.list("CSRF_TRUSTED_ORIGINS")

STATIC_URL: str = env("STATIC_URL")

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

INSTALLED_APPS: list[str] = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "djmoney",  # MoneyField
    "haystack",
    "rest_framework",
    "django_filters",
    "django_bootstrap_icons",
    "django_extensions",
    "taggit",
    "django_bootstrap5",
    "django_select2",
    "debug_toolbar",
    "mptt",
    "crispy_forms",
    "crispy_bootstrap5",
    "import_export",
    "widget_tweaks",
    "hlo",
]

AUTH_USER_MODEL = "hlo.User"

INSTALLED_APPS += env.list("INSTALLED_APPS", default=[])

MIDDLEWARE: list[str] = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "hlo.utils.custompersistentremoteusermiddleware.CustomPersistentRemoteUserMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF: str = "hlo.urls"

TEMPLATES: list[dict[str, Any]] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            (Path(BASE_DIR, "hlo", "templates")),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION: str = "hlo.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS: list[dict[str, Any]] = [
    {
        "NAME": "django.contrib.auth.password_validation."
        "UserAttributeSimilarityValidator",
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        ),
        "OPTIONS": {
            "min_length": env("PASSWORD_MIN_LEN"),
        },
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.NumericPasswordValidator"
        ),
    },
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD: str = "django.db.models.BigAutoField"

BOOTSTRAP5 = {  # We need bootstrap >= 5.3 for dark mode
    "css_url": {
        "url": "https://cdn.jsdelivr.net/npm/bootstrap@5.3/dist/css/bootstrap.min.css",
        # We can not add integrity, as it would break if a
        # new patch release comes. Should be static for production.
        # "integrity": "...",  # noqa: ERA001
        "crossorigin": "anonymous",
    },
    "javascript_url": {
        "url": "https://cdn.jsdelivr.net/npm/bootstrap@5.3/dist/js/bootstrap.bundle.min.js",
        # We can not add integrity, as it would break if a
        # new patch release comes. Should be static for production.
        # "integrity": "...",  # noqa: ERA001
        "crossorigin": "anonymous",
    },
}

db_cache = "non-default"
file_cache = "default"

if PROD:
    (db_cache, file_cache) = (file_cache, db_cache)

CACHES = {
    db_cache: {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "hlo_django_default_cache",
    },
    file_cache: {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "/tmp/django_cache",  # noqa: S108
    },
}

# run `python ./manage.py graph_models` to update hlo_model_graph.png
GRAPH_MODELS = {
    "group_models": True,
    "app_labels": ["hlo"],
    "exclude_models": ["ColorTagBase", "GenericTaggedItemBase", "TagBase"],
    "output": "model_graph.png",
    "color_code_deletions": True,
    "arrow_shape": "normal",
    "rankdir": "TB",
    "theme": "django2018",
}

DEBUG_TOOLBAR_CONFIG = {
    # "DISABLE_PANELS": {"debug_toolbar.panels.staticfiles.StaticFilesPanel"}
}

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

BS_ICONS_CACHE: Path = (MEDIA_ROOT / Path("icon_cache")).resolve()
if not BS_ICONS_CACHE.is_dir():
    BS_ICONS_CACHE.mkdir(exist_ok=True)

BARCODE_CACHE: Path = (MEDIA_ROOT / Path("barcode_cache")).resolve()
if not BARCODE_CACHE.is_dir():
    BARCODE_CACHE.mkdir(exist_ok=True)

MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.RemoteUserBackend",
]

# For CustomPersistentRemoteUserMiddleware
REMOTE_USER_HEADER = env("REMOTE_USER_HEADER")
