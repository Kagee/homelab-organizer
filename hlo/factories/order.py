import pprint

from django.contrib import admin
from django.db import models
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.html import escape, format_html, format_html_join, mark_safe
from djmoney.models.fields import MoneyField

from .attachment import Attachment
from .order import Order
