import logging

import django_filters  # type: ignore[import-untyped]  # type: ignore[import-untyped]
from django.db.models import Q

from hlo.filters.orderdaterangefilter import OrderDateRangeFilter
from hlo.models import OrderItem, Shop

logger = logging.getLogger(__name__)


class NonOrderingOrderItemFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        label="Name",
        lookup_expr="icontains",
    )
    date_range = OrderDateRangeFilter(
        label="Time range",
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
    # https://django-filter.readthedocs.io
    # /en/main/guide/tips.html#using-initial-values-as-defaults
    def __init__(self, data=None, *args, **kwargs):
        # if filterset is bound, use initial values as defaults
        if data is not None:
            # get a mutable copy of the QueryDict
            data = data.copy()

            for name, f in self.base_filters.items():
                initial = f.extra.get("initial")

                # filter param is either missing or empty,
                # use initial as default
                if not data.get(name) and initial:
                    data[name] = initial

        super().__init__(data, *args, **kwargs)

    ordering = django_filters.OrderingFilter(
        label="Order by",
        empty_label=None,
        null_label=None,
        # tuple-mapping retains order
        choices=(
            ("-order__date", "Newest order first"),
            ("order__date", "Oldest order first"),
            ("-total_nok", "Total (high to low(none))"),
            ("total_nok", "Total (low (none) to high)"),
            ("name", "Name (ABZ)"),
            ("-name", "Name (ZYX)"),
        ),
    )

    STOCKITEM_CHOICES = (
        ("hide_if_stockitems", "W/o stockitems"),
        ("show_both", "W & W/o stockitems"),
        ("show_only_if_stockitems", "W. stockitems"),
    )

    stockitem_show = django_filters.ChoiceFilter(
        choices=STOCKITEM_CHOICES,
        label="Stockitems",
        method="filter_stockitems",
        empty_label=None,
        initial="hide_if_stockitems",
    )

    def filter_stockitems(self, queryset, _name, value):
        if value == "show_both":
            return queryset
        if value == "show_only_if_stockitems":
            return queryset.filter(stockitems__isnull=False)
        # hide_if_stockitems
        return queryset.filter(stockitems__isnull=True)

    HIDDEN_CHOICES = (
        ("hide", "Hide"),
        ("both", "Both"),
        ("only", "Only"),
    )

    hidden = django_filters.ChoiceFilter(
        choices=HIDDEN_CHOICES,
        label="Hidden",
        method="filter_hidden",
        empty_label=None,
        initial="hide",
    )

    def filter_hidden(self, queryset, _name, value):
        if value == "both":
            return queryset
        if value == "only":
            return queryset.filter(Q(meta__isnull=False) & Q(meta__hidden=True))
        return queryset.filter(Q(meta__isnull=True) | Q(meta__hidden=False))
