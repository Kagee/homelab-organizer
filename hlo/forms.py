import logging

from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    HTML,
    Column,
    Div,
    Field,
    Layout,
    Row,
    Submit,
)
from django import forms
from django.forms import ModelForm, inlineformset_factory, modelformset_factory
from django.forms.widgets import DateInput, HiddenInput
from django_bootstrap_icons.templatetags.bootstrap_icons import bs_icon
from django_select2.forms import ModelSelect2TagWidget
from taggit.models import Tag

from hlo.models import Attachement, Order, OrderItem, Shop, StockItem

logger = logging.getLogger(__name__)


class TagChoices(ModelSelect2TagWidget):
    queryset = Tag.objects.all().order_by("name")
    search_fields = ["name__icontains"]
    empty_label = "Start typing to search or create tags..."

    def get_model_field_values(self, value) -> dict:
        return {"name": value}

    def create_option(  # noqa: PLR0913
        self,
        name,
        value,
        label,
        _selected,
        index,
        subindex=None,
        attrs=None,
    ):
        # if there are *any* options, set them as selected="selected", as
        # that is how we specify initial values while using ajax data
        # https://github.com/codingjoe/django-select2/issues/4#issuecomment-2106265109
        selected = "selected"
        return super().create_option(
            name,
            value,
            label,
            selected,
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
class ShopForm(ModelForm):
    class Meta:
        model = Shop
        fields = [
            "name",
            "branch_name",
            "icon",
            "order_url_template",
            "item_url_template",
        ]

    def __init__(self, *args, **kwargs):
        # We need this so self.fields is populated
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-2"
        self.helper.field_class = "col-10"


class RealDateInput(DateInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_type = "date"


class AttachementForm(ModelForm):
    class Meta:
        model = Attachement
        exclude = ["comment", "text", "manual_input", "sha1"]  # noqa: DJ006
        widgets = {}
        labels = {}
        help_texts = {}


AttachementFormSet = modelformset_factory(
    model=Attachement,
    form=AttachementForm,
    extra=1,
)


class AttachementFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = "POST"
        self.form_class = "form-vertical"
        self.label_class = "col"
        self.field_class = "col"
        self.render_required_fields = True
        self.form_tag = False
        self.add_layout(
            Column(
                Row(
                    Column(Field("name")),
                    Column(
                        Field("type"),
                    ),
                    Column(Field("file")),
                ),
            ),
        )


class OrderFormSimple(ModelForm):
    class Meta:
        model = Order
        exclude = ["manual_input", "extra_data", "attachements"]  # noqa: DJ006
        widgets = {
            "shop": HiddenInput(),
            "date": RealDateInput(),
        }
        labels = {
            "order_id": "ID",
            "date": "Date",
        }
        help_texts = {
            "order_id": None,
        }

    def __init__(self, *args, **kwargs):
        # We need this so self.fields is populated
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "form-vertical"
        self.helper.label_class = "col"
        self.helper.field_class = "col"
        self.helper.form_tag = False
        # self.helper.add_input(Submit("submit", "Create"))

        self.helper.add_layout(
            Column(
                Row(
                    Column(Field("order_id")),
                    Column(
                        Field("date"),
                    ),
                    Column(FieldWithButtons("total")),
                ),
            ),
        )


# Create the form class.
class OrderForm(ModelForm):
    class Meta:
        model = Order
        exclude = ["manual_input"]
        # fields = [
        #    "name",
        #    "branch_name",
        #    "icon",
        #    "order_url_template",
        #    "item_url_template",
        # ]

    def __init__(self, *args, **kwargs):
        # We need this so self.fields is populated
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-2"
        self.helper.field_class = "col-10"


# Create the form class.
class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        exclude = ["manual_input", "sha1_id"]
        # fields = [
        #    "name",
        #    "branch_name",
        #    "icon",
        #    "order_url_template",
        #    "item_url_template",
        # ]

    def __init__(self, *args, **kwargs):
        # We need this so self.fields is populated
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-2"
        self.helper.field_class = "col-10"


# Create the form class.
class StockItemForm(ModelForm):
    class Meta:
        model = StockItem
        fields = [
            "name",
            "count",
            "count_unit",
            "tags",
            "category",
            "project",
            "storage",
            "orderitems",
            "attachements",
            "thumbnail",
        ]

        widgets = {
            "tags": TagChoices(
                data_view="stockitem-tag-auto-json",
                attrs={
                    "data-token-separators": ",",
                },
            ),
            "name": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, initial_tags=None, **kwargs):
        if initial_tags is None:
            initial_tags = []

        # We need this so self.fields is populated
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-2"
        self.helper.field_class = "col-10"

        self.fields["tags"].widget.choices = initial_tags

        self.helper.layout = Layout(
            FieldWithButtons(
                "name",
                StrictButton(
                    bs_icon("keyboard"),
                    css_id="keyboard_btn",
                    css_class="btn btn-primary",
                    data_bs_toggle="modal",
                    data_bs_target="#keyboardModel",
                ),
            ),
            Row(
                Column(
                    HTML("Count"),
                    css_class="col-2",  # Column 2
                ),
                Column(
                    Div(
                        Field(
                            "count",
                            css_class="field-count",
                            template="crispy_raw_field.html",
                        ),
                        FieldWithButtons(
                            Field(
                                "count_unit",
                                css_class="field-count-unit",
                                template="crispy_raw_field.html",
                            ),
                            StrictButton(
                                bs_icon("plus-circle"),
                                css_id="unit_btn",
                                css_class="btn btn-primary",
                                data_bs_toggle="modal",
                                data_bs_target="#unitModal",
                            ),
                            input_size="fwb-1 w-50",
                            css_class="fwb-2",
                            template="crispy_raw_field.html",
                        ),
                        css_class="input-group",
                    ),
                    css_class="col-10",  # Column 2
                ),
                css_class="mb-3",  # Row
            ),
            Field("tags"),
            Field("thumbnail"),
            Field(
                "category",
                css_class="multiselect-dropdown-upgrade multiselect-search",
            ),
            Field(
                "project",
                css_class="multiselect-dropdown-upgrade multiselect-search",
            ),
            Field(
                "storage",
                css_class="multiselect-dropdown-upgrade multiselect-search",
            ),
            Field("orderitems"),
            Field(
                "attachements",
                css_class="multiselect-dropdown-upgrade multiselect-search",
            ),
            HTML('<p class="text-end">'),
            Submit("submit", "{{ title }}"),
            HTML("</p>"),
        )
