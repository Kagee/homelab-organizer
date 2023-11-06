from django.urls import path

from . import views

urlpatterns = [
    path('orderitems', views.product_list, name="orderitems-list"),
]