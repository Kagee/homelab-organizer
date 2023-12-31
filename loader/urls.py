from django.urls import path

from . import views
from .views import OrderItemDetailView, OrderDetailView, OrderListView

urlpatterns = [
    path('orderitems/list', views.product_list, name="orderitems-list"),
    path('orderitems/detail/<int:pk>', OrderItemDetailView.as_view(), name="orderitem"),
    path('order/list', OrderListView.as_view(), name="orders-list"),
    path('order/detail/<int:pk>', OrderDetailView.as_view(), name="order-detail"),
]
