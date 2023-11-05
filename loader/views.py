from django.shortcuts import render


# views.py
from django.views.generic import ListView
from loader.models import OrderItem

class OrderItemListView(ListView):
    model = OrderItem
    context_object_name = "order_items"
    paginate_by = 2