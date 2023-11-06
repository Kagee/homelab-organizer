import django_filters

from .models import OrderItem

class OrderItemFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = OrderItem
        fields = { 
            'order__shop': ['exact'], 
            }