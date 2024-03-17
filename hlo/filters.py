import django_filters  # type: ignore[import-untyped]
from django.db.models import Max, Min
from django.db.utils import OperationalError
from django.utils.timezone import now

from .models import Order, OrderItem, Shop


class OrderDateRangeFilter(django_filters.DateRangeFilter):
    order_choices = [
        ("month", "This month"),
        (f"year-{now().year}", "This year"),
        (f"year-{now().year-1}", "Previous year"),
    ]

    order_filters = {
        "month": lambda qs, name: qs.filter(
            **{
                "%s__year" % name: now().year,
                "%s__month" % name: now().month,
            },
        ),
        f"year-{now().year}": lambda qs, name: qs.filter(
            **{
                "%s__year" % name: now().year,
            },
        ),
        f"year-{now().year-1}": lambda qs, name: qs.filter(
            **{
                "%s__year" % name: now().year - 1,
            },
        ),
    }

    # pylint: disable=keyword-arg-before-vararg
    def __init__(self, _choices=None, _filters=None, *args, **kwargs):
        this_year = now().year
        try:
            order_years = Order.objects.aggregate(
                Max("date__year"),
                Min("date__year"),
            )
        except OperationalError:
            order_years = {}
            order_years["date__year__max"] = this_year
            order_years["date__year__min"] = this_year - 1

        if (
            "date__year__max" not in order_years
            or not order_years["date__year__max"]
        ):
            order_years["date__year__max"] = this_year
        if (
            "date__year__min" not in order_years
            or not order_years["date__year__min"]
        ):
            order_years["date__year__min"] = this_year - 1
        for year in reversed(
            range(
                order_years["date__year__min"],
                order_years["date__year__max"] + 1,
            ),
        ):
            if year in (this_year, this_year - 1):
                continue
            self.order_choices.append((f"year-{year!s}", str(year)))
            # We have to capture year in l_year,
            # if not all lambdas would use the same year value
            self.order_filters[f"year-{year!s}"] = (
                lambda qs, name, lambda_year=year: qs.filter(
                    **{
                        "%s__year" % name: lambda_year,
                    },
                )
            )
        super().__init__(
            choices=self.order_choices,
            filters=self.order_filters,
            field_name="order__date",
            *args,  # noqa: B026
            **kwargs,
        )


class OrderItemFilter(django_filters.FilterSet):
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
        label="Time",
        empty_label="All time",
    )

    order = django_filters.OrderingFilter(
        label="Order by",
        empty_label=None,
        null_label=None,
        # tuple-mapping retains order
        fields=(
            ("name", "name"),
            ("order__date", "order__date"),
        ),
    )

    order__shop = django_filters.ModelChoiceFilter(
        queryset=Shop.objects.all(),
        empty_label="All shops",
        label="Shop",
    )

    class Meta:
        model = OrderItem
        fields: dict = {}


class StockItemFilter(django_filters.FilterSet):
    name = django_filters.LookupChoiceFilter(
        label="Stock item name",
        lookup_choices=[
            ("icontains", "Contains"),
            ("istartswith", "Starts with"),
            ("iexact", "Equals"),
        ],
        empty_label=None,
    )

    class Meta:
        model = OrderItem
        fields = {
            "name",  # not suire if correct, fields is required
            # "order__shop": ["exact"],  # noqa: ERA001
        }
