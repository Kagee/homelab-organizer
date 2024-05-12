from django import forms
from django.forms import ModelForm
from django_select2.forms import ModelSelect2TagWidget
from mptt.forms import TreeNodeMultipleChoiceField
from taggit.models import Tag

from hlo.models import StockItem, Storage


class TagChoices(ModelSelect2TagWidget):
    queryset = Tag.objects.all().order_by("name")
    search_fields = ["name__icontains"]
    empty_label = "Start typing to search or create tags..."

    def get_model_field_values(self, value) -> dict:
        return {"name": value}

    def create_option(  # noqa: PLR0913
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        return super().create_option(
            name,
            value,
            label,
            # if there are *any* options, set them as selected="selected", as
            # that is how we specify initial values while using ajax data
            "selected",
            index,
            subindex,
            attrs,
        )

    def value_from_datadict(self, data, files, name):
        """Create objects for missing tags.

        Return comma separates string of tags.
        """
        values = set(super().value_from_datadict(data, files, name))
        names = self.queryset.filter(name__in=list(values)).values_list(
            "name",
            flat=True,
        )
        names = set(map(str, names))
        cleaned_values = list(names)
        # if a value is not in names (tag with name does
        # not exists), it has to be created
        cleaned_values += [
            self.queryset.create(name=val).name for val in (values - names)
        ]
        # django-taggit expects a comma-separated list
        return ",".join(cleaned_values)


# Create the form class.
class StockItemForm(ModelForm):
    class Meta:
        model = StockItem
        fields = [
            "name",
            "count",
            "tags",
            "orderitems",
            "category",
            "project",
            "storage",
        ]

        widgets = {
            "tags": TagChoices(
                data_view="stockitem-tag-auto-json",
                attrs={"data-token-separators": ","},
            ),
            "name": forms.Textarea(attrs={"rows": 3}),
        }
