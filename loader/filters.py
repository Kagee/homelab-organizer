import django_filters

from .models import OrderItem

class OrderItemFilter(django_filters.FilterSet):
    name = django_filters.LookupChoiceFilter(
         lookup_choices=[
        ('icontains', 'Contains'),
        ('istartswith', 'Starts with'),
        ('iexact', 'Equals'),
    ],
    )

    year = django_filters.AllValuesFilter(field_name='order__date', lookup_expr='year')
    class Meta:
        model = OrderItem
        fields = {
            'order__shop': ['exact'],
            #'order__date': ['year'],
            }
