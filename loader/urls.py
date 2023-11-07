from django.urls import path

from . import views
from .views import OrderItemDetailView

urlpatterns = [
    path('orderitems', views.product_list, name="orderitems-list"),
    path('orderitems/<int:pk>', OrderItemDetailView.as_view(), name="orderitem"),
]
