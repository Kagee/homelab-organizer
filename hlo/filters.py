# import logging
from datetime import datetime
import django_filters
from django.db.models import Max, Min
from django.db.utils import OperationalError
from .models import OrderItem, Order


class OrderDateRangeFilter(django_filters.DateRangeFilter):
    order_choices = [
        ("month", "This month"),
        (f"year-{datetime.now().year}", "This year"),
        (f"year-{datetime.now().year-1}", "Previous year"),
    ]

    order_filters = {
        "month": lambda qs, name: qs.filter(
            **{
                "%s__year" % name: datetime.now().year,
                "%s__month" % name: datetime.now().month,
            }
        ),
        f"year-{datetime.now().year}": lambda qs, name: qs.filter(
            **{
                "%s__year" % name: datetime.now().year,
            }
        ),
        f"year-{datetime.now().year-1}": lambda qs, name: qs.filter(
            **{
                "%s__year" % name: datetime.now().year - 1,
            }
        ),
    }

    # pylint: disable=keyword-arg-before-vararg
    def __init__(self, choices=None, filters=None, *args, **kwargs):
        this_year = datetime.now().year
        try:
            order_years = Order.objects.aggregate(
                Max("date__year"), Min("date__year")
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
            )
        ):
            if year in (this_year, this_year - 1):
                continue
            self.order_choices.append((f"year-{str(year)}", str(year)))
            # We have to capture year in l_year, if not all lambdas would use the same year value
            self.order_filters[f"year-{str(year)}"] = (
                lambda qs, name, lambda_year=year: qs.filter(
                    **{
                        "%s__year" % name: lambda_year,
                    }
                )
            )
        super().__init__(
            choices=self.order_choices,
            filters=self.order_filters,
            field_name="order__date",
        )


class OrderItemFilter(django_filters.FilterSet):
    name = django_filters.LookupChoiceFilter(
        lookup_choices=[
            ("icontains", "Contains"),
            ("istartswith", "Starts with"),
            ("iexact", "Equals"),
        ],
        empty_label=None,
    )

    order_date_year_range = OrderDateRangeFilter()

    o = django_filters.OrderingFilter(
        label="Order by",
        empty_label=None,
        null_label=None,
        # tuple-mapping retains order
        fields=(
            ("name", "name"),
            ("order__date", "order__date"),
        ),
        # field_labels={
        #    'name': 'Title',
        # }
    )

    class Meta:
        model = OrderItem
        fields = {
            "order__shop": ["exact"],
        }
