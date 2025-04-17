import django_filters  # type: ignore[import-untyped]
from django.db.models import Max, Min
from django.db.utils import OperationalError, ProgrammingError
from django.utils.timezone import now

from hlo.models import Order


class OrderDateRangeFilter(django_filters.DateRangeFilter):
    order_choices = [
        ("month", "This month"),
        (f"year-{now().year}", "This year"),
        (f"year-{now().year - 1}", "Previous year"),
    ]

    order_filters = {
        "month": lambda qs, name: qs.filter(
            **{
                "%s__year" % name: now().year,  # noqa: UP031
                "%s__month" % name: now().month,  # noqa: UP031
            },
        ),
        f"year-{now().year}": lambda qs, name: qs.filter(
            **{
                "%s__year" % name: now().year,  # noqa: UP031
            },
        ),
        f"year-{now().year - 1}": lambda qs, name: qs.filter(
            **{
                "%s__year" % name: now().year - 1,  # noqa: UP031
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
        except (OperationalError, ProgrammingError):
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
                        "%s__year" % name: lambda_year,  # noqa: UP031
                    },
                )
            )
        super().__init__(
            choices=self.order_choices,
            filters=self.order_filters,
            # take this from constructor, thus we
            # can use it both for orderitem and stockitem
            # field_name
            *args,  # noqa: B026
            **kwargs,
        )
