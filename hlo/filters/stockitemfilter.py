import django_filters  # type: ignore[import-untyped]

from hlo.models import Shop, StockItem

from .orderitemfilter import OrderDateRangeFilter


class StockItemFilter(django_filters.FilterSet):
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
        field_name="orderitem__order__date",
    )

    shop = django_filters.ModelChoiceFilter(
        queryset=Shop.objects.all(),
        field_name="orderitem__order__shop",
        empty_label="All shops",
        label="Shop",
    )

    ordering = django_filters.OrderingFilter(
        label="Order by",
        empty_label=None,
        null_label=None,
        # tuple-mapping retains order
        fields=(
            ("name", "name"),
            ("orderitem__order__date", "orderitem__order__date"),
        ),
    )

    class Meta:
        model = StockItem
        fields = {
            "name",  # not suire if correct, fields is required
            # "order__shop": ["exact"],  # noqa: ERA001
        }
