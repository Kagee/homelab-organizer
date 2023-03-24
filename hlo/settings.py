"""
Django settings for hlo project.
"""

import os
from pathlib import Path
from typing import List, Dict, Any
import environ  # type: ignore

env = environ.FileAwareEnv(
    # set casting, default value
    HLO_DEBUG=(bool, False),
    HLO_ALLOWED_HOSTS=(list, []),
    # https://docs.djangoproject.com/en/3.2/topics/i18n/
    HLO_LANGUAGE_CODE=(str, "en-us"),
    HLO_TIME_ZONE=(str, "UTC"),
    HLO_USE_I18N=(bool, False),
    HLO_USE_L10N=(bool, False),
    HLO_USE_TZ=(bool, True),
)
env.prefix = 'HLO_'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR: Path = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

DEBUG: bool = env('DEBUG')

LANGUAGE_CODE: str = env('LANGUAGE_CODE')
TIME_ZONE: str = env('TIME_ZONE')
USE_I18N: bool = env('USE_I18N')
USE_L10N: bool = env('USE_L10N')
USE_TZ: bool = env('USE_TZ')

# Raises Django's ImproperlyConfigured
# exception if SECRET_KEY not in os.environ
SECRET_KEY: str = env('SECRET_KEY')

# Parse database connection url strings
DATABASES = {
    # read os.environ['DATABASE_URL'] and raises
    # ImproperlyConfigured exception if not found
    'default': env.db(),
}


ALLOWED_HOSTS: List[str] = env('ALLOWED_HOSTS')
# Application definition

INSTALLED_APPS: List[str] = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE: List[str] = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF: str = "hlo.urls"

TEMPLATES: List[Dict[str, Any]] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

AUTH_PASSWORD_VALIDATORS: List[Dict[str, str]] = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL: str = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD: str = "django.db.models.BigAutoField"
