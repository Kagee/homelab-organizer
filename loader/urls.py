from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path("orderitems", OrderItemListView.as_view(), name="orderitem-list"),
]