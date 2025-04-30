import logging

from crispy_forms.bootstrap import (  # type: ignore[import-untyped]
    FieldWithButtons,
)
from crispy_forms.helper import FormHelper  # type: ignore[import-untyped]
from crispy_forms.layout import (  # type: ignore[import-untyped]
    Column,
    Field,
    Row,
)
from django.forms import ModelForm
from django.forms.widgets import DateInput, HiddenInput

from hlo.models import Order

logger = logging.getLogger(__name__)


class RealDateInput(DateInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_type = "date"


class OrderFormSimple(ModelForm):
    class Meta:
        model = Order
        exclude = ["manual_input", "extra_data", "attachments"]  # noqa: DJ006
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
                    Column(Field("date")),
                    Column(FieldWithButtons("total")),
                ),
            ),
        )


# Create the form class.
class OrderForm(ModelForm):
    class Meta:
        model = Order
        exclude = ["manual_input"]  # noqa: DJ006

    def __init__(self, *args, **kwargs):
        # We need this so self.fields is populated
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-2"
        self.helper.field_class = "col-10"
