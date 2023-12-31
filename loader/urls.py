from django.urls import path

from . import views
from .views import OrderItemDetailView

urlpatterns = [
    path('orderitems/list', views.product_list, name="orderitems-list"),
    path('orderitems/detail/<int:pk>', OrderItemDetailView.as_view(), name="orderitem"),
]
