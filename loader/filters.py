import django_filters

from .models import OrderItem

class OrderItemFilter(django_filters.FilterSet):
    name = django_filters.LookupChoiceFilter(
        #field_class=django_filters.CharFilter,
         lookup_choices=[
        ('icontains', 'Contains'),
        ('istartswith', 'Starts with'),
        ('iexact', 'Equals'),
    ],
    #empty_label='Contains',
    #empty_value='icontains',
    
    label="exact",
    # lookup_expr=('icontains', 'Contains'),
    # required=True,
    
    # # Field.__init__() got an unexpected keyword argument '...'
    # null_value='icontains',
    # default=('icontains', 'Contains'), 
    # default='icontains',

    )
    # fields = (field, ChoiceField(choices=lookup_choices, empty_label=empty_label))
    #     widget = LookupChoiceWidget(widgets=[f.widget for f in fields])
    #name.field.

    year = django_filters.AllValuesFilter(field_name='order__date', lookup_expr='year')
    class Meta:
        model = OrderItem
        fields = {
            'order__shop': ['exact'],
            #'order__date': ['year'],
            }
