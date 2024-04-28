import django_filters  # type: ignore[import-untyped]  # type: ignore[import-untyped]

from hlo.filters.orderdaterangefilter import OrderDateRangeFilter
from hlo.models import OrderItem, Shop


class NonOrderingOrderItemFilter(django_filters.FilterSet):
    name = django_filters.LookupChoiceFilter(
        label="Name",
        lookup_choices=[
            ("icontains", "Contains"),
            ("istartswith", "Starts with"),
            ("iexact", "Equals"),
        ],
        empty_label=None,
    )

    date_range = OrderDateRangeFilter(
        label="Timerange",
        empty_label="All time",
        field_name="order__date",
    )

    shop = django_filters.ModelChoiceFilter(
        queryset=Shop.objects.all(),
        field_name="order__shop",
        empty_label="All shops",
        label="Shop",
    )

    class Meta:
        model = OrderItem
        fields: dict = {}


class OrderItemFilter(NonOrderingOrderItemFilter):
    ordering = django_filters.OrderingFilter(
        label="Order by",
        empty_label=None,
        null_label=None,
        # tuple-mapping retains order
        fields=(
            ("name", "name"),
            ("order__date", "order__date"),
        ),
    )
